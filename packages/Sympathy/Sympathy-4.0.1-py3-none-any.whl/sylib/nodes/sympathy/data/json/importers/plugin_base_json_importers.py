# This file is part of Sympathy for Data.
# Copyright (c) 2018, Combine Control Systems AB
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
import io
import json
from lxml import etree
from collections import defaultdict
from sympathy.api import importers
from sympathy.api import qt2 as qt_compat

QtWidgets = qt_compat.import_module('QtWidgets')


def _sniff_type(filename):
    """
    Guess if it is a JSON or XML file by looking
    at the file extension or the first line
    """
    ext = os.path.splitext(filename)[1].lower()
    if ext in [".json", ".xml"]:
        return ext[1:]

    with open(filename, "rb") as f:
        for line in f:
            line = line.lstrip()
            if line:
                if line.startswith(b"<"):
                    return "xml"
                else:
                    return "json"


def _add_nonempty_text(children, text):
    if text:
        text = text.strip()
        if text:
            children.append({'#text': text})


def _get_nsname(reverse_nsmap, obj):
    qname = etree.QName(obj)
    name = qname.localname
    namespace = qname.namespace
    if namespace and namespace in reverse_nsmap:
        ns_name = reverse_nsmap[namespace]
        if ns_name:
            name = f'{ns_name}:{name}'
    return name


def _get_attrname(nsname):
    res = '@xmlns'
    if nsname:
        res = f'@xmlns:{nsname}'
    return res


def lxml_element_to_json(element, nsmap):
    """
    Convert XML to JSON.

    - Text and tail are children with name #text.
    - Attributes are children prefixed by @.
    - Namespace declarations are treated as attributes.

    Elements without children are omitted, ones with
    1 child produces a dict, and ones with several a
    list.
    """
    children = []
    reverse_nsmap = {v: k for k, v in nsmap.items()}
    tag_key = _get_nsname(reverse_nsmap, element)
    local_nsmap = element.nsmap
    res = {tag_key: None}

    for k, v in local_nsmap.items():
        if k not in nsmap or nsmap[k] != local_nsmap[k]:
            children.append({_get_attrname(k): v})

    for k, v in element.attrib.items():
        attr_name = f'@{_get_nsname(reverse_nsmap, k)}'
        children.append({attr_name: v})

    _add_nonempty_text(children, element.text)

    for child in element:
        children.append(lxml_element_to_json(child, local_nsmap))
        _add_nonempty_text(children, child.tail)

    len_children = len(children)
    if len_children == 1 and '#text' in children[0]:
        res[tag_key] = list(children[0].values())[0]
    elif len_children > 1:
        data = {}
        res[tag_key] = data
        counts = defaultdict(int)
        for child in children:
            for k, v in child.items():
                counts[k] += 1

        for k, count in counts.items():
            if count > 1:
                data[k] = []

        for child in children:
            for k, v in child.items():
                count = counts[k]
                if count > 1:
                    data[k].append(v)
                else:
                    data[k] = v
    return res


def lxml_file_to_json(f):
    etree_parse = etree.parse(f)
    root = etree_parse.getroot()
    return lxml_element_to_json(root, {})


def import_data(obj, filename, filetype):
    """
    Load a Json structure from a datasource or a filepath

    :param datasource: the datasource or the filepath to load the Json from
    :param filetype: can be either ``json`` or ``xml`` and determines what type
                     of file to load
    """
    filetype = filetype.lower()
    with io.open(filename, "rb") as f:
        if filetype == "json":
            _dict = json.load(f)
        elif filetype == "xml":
            _dict = lxml_file_to_json(f)
        else:
            assert False, 'Unknown filetype'
    obj.set(_dict)


class DataImportAuto(importers.AutoImporterMixin,
                     importers.JsonDataImporterBase):

    IMPORTER_NAME = "Auto"
    _IMPORTER_BASE = importers.JsonDataImporterBase


class DataImportXml(importers.JsonDataImporterBase):
    IMPORTER_NAME = "XML"

    def valid_for_file(self):
        try:
            return _sniff_type(self._fq_infilename) == 'xml'
        except Exception:
            return False

    def parameter_view(self, parameters):
        if not self.valid_for_file():
            return QtWidgets.QLabel(
                'File does not exist or cannot be read.')
        return QtWidgets.QLabel()

    def import_data(self, out_datafile, parameters=None, progress=None):
        try:
            import_data(out_datafile, self._fq_infilename, filetype='xml')
        except Exception as e:
            raise self.import_failed(e)


class DataImportJson(importers.JsonDataImporterBase):
    IMPORTER_NAME = "JSON"

    def valid_for_file(self):
        try:
            return _sniff_type(self._fq_infilename) == 'json'
        except Exception:
            return False

    def parameter_view(self, parameters):
        if not self.valid_for_file():
            return QtWidgets.QLabel(
                'File does not exist or cannot be read.')
        return QtWidgets.QLabel()

    def import_data(self, out_datafile, parameters=None, progress=None):
        try:
            import_data(out_datafile, self._fq_infilename, filetype='json')
        except Exception as e:
            raise self.import_failed(e)
