# This file is part of Sympathy for Data.
# Copyright (c) 2013, Combine Control Systems AB
#
# Sympathy for Data is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Sympathy for Data is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sympathy for Data.  If not, see <http://www.gnu.org/licenses/>.
import os
import sys
import signal
import subprocess
import fnmatch

import pytest

from sympathy.platform import workflow_converter
from sympathy.utils import prim


TIMEOUT = 60 * 4


def collect_call(args, timeout, pipe_workflows=None, **kwargs):
    """Calls args, returning the exit code and stdout as a string."""
    process = None
    exitcode = None

    try:
        close_fds = prim.is_posix()
        if pipe_workflows:
            pipe_workflows = list(pipe_workflows)
            pipe_workflows.extend(['', ''])

            process = subprocess.Popen(
                args, stdin=subprocess.PIPE, bufsize=1,
                universal_newlines=True, close_fds=close_fds,
                **kwargs)
            process.communicate(input='\n'.join(pipe_workflows))
        else:
            process = subprocess.Popen(
                args, stdin=subprocess.PIPE, bufsize=1,
                universal_newlines=True, close_fds=close_fds,
                **kwargs)
            process.communicate()
        exitcode = process.poll()
    except Exception:
        import traceback
        traceback.print_exc()
        if process is not None:
            if sys.platform == 'win32':
                process.kill()
            else:
                os.kill(-process.pid, signal.SIGKILL)
        raise

    if exitcode != 0:
        raise subprocess.CalledProcessError(
            exitcode, 'Sympathy exited with a non-zero exitcode.')


def run_workflow(args, pipe_workflows=None, **kwargs):
    """
    Returns a function which runs the workflow as required by nosetest's
    generator interface.
    The function will have its description attribute set to the name of the
    workflow. This will be presented as the test name by nosetest.
    """

    env = dict(os.environ)
    env['SY_TEST_RUN'] = '1'

    def inner():
        if pipe_workflows:
            workflows = pipe_workflows
            collect_call(
                [sys.executable, '-m', 'sympathy', 'cli', '-L', '4',
                 '--num-worker-processes', '1', '-'], TIMEOUT, workflows,
                env=env,
                **kwargs)
        else:
            # This will not work in cli mode.
            collect_call(
                [sys.executable, '-m', 'sympathy', 'cli', '-L', '4',
                 '--num-worker-processes', '1'] + args, TIMEOUT,
                env=env,
                **kwargs)

    try:
        filename = args[0]
    except IndexError:
        filename = ''

    desc = 'Test WF {}'.format(os.path.basename(filename))

    inner.description = desc
    return inner


def _flow_should_run(flow_path):
    with open(flow_path, 'rb') as f:
        flow_dict = workflow_converter.XMLToJson(f).dict()
        return 'NO_TEST' not in flow_dict.get('environment', {})


def find_flows(test_dir):
    flows = []
    ids = []
    for dirpath, dirnames, filenames in os.walk(test_dir):
        for filename in fnmatch.filter(filenames, '*.syx'):
            flow = os.path.join(dirpath, filename)
            if _flow_should_run(flow):
                flows.append(flow)
                try:
                    rel_path = os.path.relpath(flow, test_dir)
                except Exception:
                    rel_path = flow
                ids.append(rel_path)
    return flows, ids


class SympathyFlowRunner():
    _max_processes = 5

    def __init__(self):
        self._proc = None
        self._started_processes = 0

    def _start_sympathy(self):
        env = dict(os.environ)
        env['SY_TEST_RUN'] = '1'
        args = [sys.executable, '-m', 'sympathy', 'cli', '-L', '4',
                '--num-worker-processes', '1', '-']
        close_fds = prim.is_posix()

        self._proc = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True,
            close_fds=close_fds,
        )
        self._started_processes += 1

    def _ensure_sympathy(self):
        if self._proc is None or self._proc.poll() is not None:
            if self._started_processes > self._max_processes:
                pytest.skip(
                    f"Refusing to start more than {self._max_processes} "
                    f"Sympathy processes.")
            self._start_sympathy()

    def run(self, flow_path):
        self._ensure_sympathy()

        self._proc.stdin.write(flow_path + '\n')
        self._proc.stdin.flush()

        while True:
            line = self._proc.stdout.readline()
            if not line:
                self._proc.wait()
                return self._proc.returncode
            elif line.startswith('INFO:core:Flow successfully executed'):
                return 0
            elif not line.startswith('INFO:core:Start processing flow'):
                print(line, end='')

    def stop(self):
        self._proc.communicate('\n')


@pytest.fixture(scope="session")
def sy_flow_runner():
    """
    Return a class handling a Sympathy for Data process suitable for running
    flows.
    """
    runner = SympathyFlowRunner()
    yield runner
    runner.stop()


def run_flows_in_path(path, prefix='Test flow '):
    flows, _ = find_flows(path)
    if not flows:
        return

    def start_sympathy():
        env = dict(os.environ)
        env['SY_TEST_RUN'] = '1'
        args = [sys.executable, '-m', 'sympathy', 'cli', '-L', '4',
                '--num-worker-processes', '1', '-']
        close_fds = prim.is_posix()

        process = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True,
            close_fds=close_fds,
        )

        return process

    proc = start_sympathy()
    started_processes = 1
    for i, flow in enumerate(flows):
        test_name = prefix + os.path.relpath(flow, path)
        if proc.poll() is not None:
            if started_processes > 5:
                raise RuntimeError(
                    "Refusing to start more Sympathy processes."
                    "The following flows have not been tested:\n"
                    + "\n".join(flows[i:]))
            proc = start_sympathy()
            started_processes += 1

        def read_output():
            proc.stdin.write(flow + '\n')
            proc.stdin.flush()

            while True:
                line = proc.stdout.readline()
                print(line, end='')
                if not line:
                    proc.wait()
                    assert proc.returncode == 0
                    break
                if line.startswith('INFO:core:Flow successfully executed'):
                    break
        read_output.description = test_name
        yield read_output
    proc.communicate('\n')
