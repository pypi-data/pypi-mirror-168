# This file is part of Sympathy for Data.
# Copyright (c) 2022, Combine Control Systems AB
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
import os.path

from sympathy.api import typeutil


_dirname = os.path.abspath(os.path.dirname(__file__))


def is_bokeh(scheme, filename):
    return File.is_type(filename, scheme)


def _bokeh():
    # Delay import of bokeh in case it takes time
    import bokeh
    import bokeh.models
    import bokeh.plotting
    import bokeh.embed
    import bokeh.resources
    import bokeh.settings
    bokeh.settings.settings.simple_ids = False
    return bokeh


def new_bokeh_figure(*args, **kwargs):
    return _bokeh().plotting.figure(*args, **kwargs)


@typeutil.typeutil('sytypealias bokeh = sytext')
class File(typeutil.TypeAlias):
    """
    A Bokeh Figure.

    Any node port with the *Bokeh* type will produce an object of this type.
    """
    def get_document(self):
        if not self._data.get():
            self.set_figure(new_bokeh_figure())

        return _bokeh().plotting.Document.from_json_string(self._data.get())

    def set_document(self, document):
        self._data.set(document.to_json_string())

    def get_figure(self):
        document = self.get_document()
        figure = document.roots[0]

        # Needed to allow the figure to be put in a different document later.
        document.remove_root(figure)

        return figure

    def set_figure(self, figure):
        document = _bokeh().plotting.Document()
        document.add_root(figure)
        self.set_document(document)

    @classmethod
    def viewer(cls):
        from . import bokeh_viewer
        return bokeh_viewer.BokehViewer

    @classmethod
    def icon(cls):
        return os.path.join(_dirname, 'bokeh.svg')

    def save_figure(self, filename, use_cdn=False, stretch=False):
        """
        Save figure to an html file.

        Parameters
        ----------
        filename : pathlike
            The path where the file will be saved.
        use_cdn : bool, optional
            If True, required bokeh resources (js and css files) will be linked
            to the official bokeh cdn server. If False (the default), those
            resources are instead inlined in the html file.
        stretch : bool, optional
            If True, set sizing_mode='stretch_both' for the figure before
            saving. This makes the figure always occupy the entire browser
            window.
        """
        resources = (_bokeh().resources.CDN
                     if use_cdn
                     else _bokeh().resources.INLINE)
        figure = self.get_figure()
        if stretch:
            figure.sizing_mode = 'stretch_both'

            # HACK: (Magnus 2022-05-30) Since Plot also inherits from
            # LayoutDOM, I'm not sure how else we could know that this is a
            # layout of several plots.
            if not isinstance(figure, _bokeh().models.Plot):
                for child_tuple in figure.children:
                    child_tuple[0].sizing_mode = 'stretch_both'

        html = _bokeh().embed.file_html(figure, resources)

        with open(filename, 'w') as f:
            f.write(html)
