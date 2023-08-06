"""
This module represents the whole report builder.
A report can contain many pages, and each page can contain many items.
You can assemble different items into different pages.

The following classes are available:
    * :class:`ChartItem`
    * :class:`Page`
    * :class:`ReportBuilder`
"""

# pylint: disable=invalid-name
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-member
# pylint: disable=too-few-public-methods
# pylint: disable=super-init-not-called
# pylint: disable=attribute-defined-outside-init
from typing import List
from hana_ml.visualizers.model_report import TemplateUtil
from hana_ml.visualizers.ui_components import HTMLUtils, HTMLFrameUtils


class Item(object):
    def __init__(self):
        pass

    def to_json(self):
        return {
            'title': self.title,
            'type': self.type,
            'config': self.config
        }


class DescriptionItem(Item):
    def __init__(self, title: str):
        self.title: str = title
        self.type = 'description'
        self.config = []

    def add(self, name: str, description: str):
        if name and description:
            self.config.append({
                'name': name,
                'value': description
            })
        else:
            raise ValueError('Added name or description is none!')


class ChartItem(Item):
    """
    This item represents an chart type.

    Parameters
    ----------
    title : str
        The chart item name.

    config : json
        The chart item config.
    """
    def __init__(self, title: str, config):
        self.title: str = title
        self.type = 'chart'
        self.config = config


class TableItem(Item):
    def __init__(self, title: str, config):
        self.title: str = title
        self.type = 'table'
        self.config = config


class HTMLStringItem(Item):
    def __init__(self, title: str, config):
        self.title: str = title
        self.type = 'other'
        self.config = config


class Page(object):
    """
    Every report consists of many pages. Each page contains multiple items.

    Parameters
    ----------
    title : str
        The page name.
    """
    def __init__(self, title: str):
        self.title: str = title
        self.items: List[Item] = []

    def addItem(self, item: Item):
        """
        Add a item instance to page instance.

        Parameters
        ----------
        item : Item
            Each page contains multiple items.
        """
        if item:
            self.items.append(item.to_json())
        else:
            raise ValueError('Added item is none!')

    def addItems(self, items: List[Item]):
        """
        Add many item instances to page instance.

        Parameters
        ----------
        items : List[Item]
            Each page contains multiple items.
        """
        if items and len(items) > 0:
            for item in items:
                self.addItem(item)
        else:
            raise ValueError('Added items is none or no data items!')

    def to_json(self):
        """
        Return the config data of single page.
        This method is automatically called by the internal framework.
        """
        return {
            'title': self.title,
            'items': self.items
        }


class ReportBuilder(object):
    __TEMPLATE = TemplateUtil.get_template('report_builder.html')

    """
    This class is a report builder and the base class for report building. Can be inherited by custom report builder classes.

    Parameters
    ----------
    title : str
        The report name.
    """
    def __init__(self, title: str):
        self.title: str = title
        self.pages: List[Page] = []
        self.html = None
        self.frame_src = None
        self.frame_id = ''

    def addPage(self, page: Page):
        """
        Add a page instance to report instance.

        Parameters
        ----------
        page : Page
            Every report consists of many pages.
        """
        if page:
            self.pages.append(page.to_json())
        else:
            raise ValueError('Added page is none!')

    def addPages(self, pages: List[Page]):
        """
        Add many page instances to report instance.

        Parameters
        ----------
        pages : List[Page]
            Every report consists of many pages.
        """
        if pages and len(pages) > 0:
            for page in pages:
                self.addPage(page)
        else:
            raise ValueError('Added pages is none or no data items!')

    def to_json(self):
        """
        Return the all config data of report.
        This method is automatically called by the internal framework.
        """
        return {
            'title': self.title,
            'pages': self.pages
        }

    def build(self, debug=False):
        """
        Build HTML string based on current config.

        Parameters
        ----------
        debug : bool
            Whether the log should be printed to the console.

            Defaults to False.
        """
        if debug is False:
            debug = 'false'
        else:
            debug = 'true'
        self.html = HTMLUtils.minify(ReportBuilder.__TEMPLATE.render(debug=debug, reportConfig=self.to_json()))
        self.frame_src = HTMLFrameUtils.build_frame_src(self.html)
        self.pages = []

    def generate_html(self, filename):
        """
        Save the report as a html file.

        Parameters
        ----------
        filename : str
            HTML file name.
        """
        TemplateUtil.generate_html_file('{}_report.html'.format(filename), self.html)

    def generate_notebook_iframe(self, iframe_height=600):
        """
        Render the report as a notebook iframe.

        Parameters
        ----------
        iframe_height : int
            iframe height.

            Defaults to 600.
        """
        HTMLFrameUtils.check_frame_height(iframe_height)
        self.frame_html = HTMLFrameUtils.build_frame_html_with_id(self.frame_id, self.frame_src, iframe_height)
        HTMLFrameUtils.display(self.frame_html)
