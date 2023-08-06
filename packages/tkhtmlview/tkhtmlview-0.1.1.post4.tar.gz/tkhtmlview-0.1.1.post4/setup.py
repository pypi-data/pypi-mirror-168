# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tkhtmlview']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'tkhtmlview',
    'version': '0.1.1.post4',
    'description': 'Display HTML with Tkinter',
    'long_description': '# tkhtmlview\n\n![PyPI](https://img.shields.io/pypi/v/tkhtmlview?logo=python&style=flat-square)\n[![Publish to Pypi](https://github.com/bauripalash/tkhtmlview/actions/workflows/publish-to-pypi.yml/badge.svg)](https://github.com/bauripalash/tkhtmlview/actions/workflows/publish-to-pypi.yml)\n\nHTML widgets for tkinter\n\n> Fork of [tk_html_widgets](https://github.com/paolo-gurisatti/tk_html_widgets)\n\n## Overview\n\nThis module is a collection of tkinter widgets whose text can be set in HTML format.\nA HTML widget isn\'t a web browser frame, it\'s only a simple and lightweight HTML parser that formats the tags used by the tkinter Text base class.\nThe widgets behaviour is similar to the PyQt5 text widgets (see the [PyQt5 HTML markup subset](http://doc.qt.io/qt-5/richtext-html-subset.html)).\n\n## Installation\n\n`pip install tkhtmlview`\n\n## Requirements\n\n- [Python 3.4 or later](https://www.python.org/downloads/) with tcl/tk support\n- [Pillow 5.3.0](https://github.com/python-pillow/Pillow)\n- requests\n\n## Example\n\n```python\nimport tkinter as tk\nfrom tkhtmlview import HTMLLabel\n\nroot = tk.Tk()\nhtml_label = HTMLLabel(root, html=\'<h1 style="color: red; text-align: center"> Hello World </H1>\')\nhtml_label.pack(fill="both", expand=True)\nhtml_label.fit_height()\nroot.mainloop()\n```\n\nYou can also save html in a separate .html file and then use `RenderHTML` to render html for widgets.\n\n- _index.html_\n\n    ```html\n    <!DOCTYPE html>\n    <html>\n        <body>\n            <h1>Orange is so Orange</h1>\n            <img\n            src="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg"\n            />\n            <p>\n            The orange is the fruit of various citrus species in the family Rutaceae;\n            it primarily refers to Citrus × sinensis, which is also called sweet\n            orange, to distinguish it from the related Citrus × aurantium, referred to\n            as bitter orange.\n            </p>\n        </body>\n    </html>\n    ```\n\n- _demo.py_\n\n    ```python\n    import tkinter as tk\n    from tkhtmlview import HTMLText, RenderHTML\n\n    root = tk.Tk()\n    html_label = HTMLText(root, html=RenderHTML(\'index.html\'))\n    html_label.pack(fill="both", expand=True)\n    html_label.fit_height()\n    root.mainloop()\n    ```\n\n## Documentation\n\n### Classes\n\nAll widget classes inherits from the tkinter.Text() base class.\n\n#### class HTMLScrolledText(tkinter.Text)\n\n> Text-box widget with vertical scrollbar\n\n#### class HTMLText(tkinter.Text)\n\n> Text-box widget without vertical scrollbar\n\n#### class HTMLLabel(tkinter.Text)\n\n> Text-box widget with label appearance\n\n#### class RenderHTML\n\n> RenderHTML class will render HTML from .html file for the widgets.\n\n### Methods\n\n#### def set_html(self, html, strip=True)\n\n> **Description:** Sets the text in HTML format. <br> > **Args:**\n>\n> - _html_: input HTML string\n> - _strip_: if True (default) handles spaces in HTML-like style\n\n#### def fit_height(self)\n\n> **Description:** Fit widget height in order to display all wrapped lines\n\n### HTML support\n\nOnly a subset of the whole HTML tags and attributes are supported (see table below).\nWhere is possibile, I hope to add more HTML support in the next releases.\n\n| **Tags** | **Attributes**     | **Notes**                              |\n| -------- | ------------------ | -------------------------------------- |\n| a        | style, href        |\n| b        | style              |\n| br       |                    |\n| code     | style              |\n| div      | style              |\n| em       | style              |\n| h1       | style              |\n| h2       | style              |\n| h3       | style              |\n| h4       | style              |\n| h5       | style              |\n| h6       | style              |\n| i        | style              |\n| img      | src, width, height | experimental support for remote images |\n| li       | style              |\n| mark     | style              |\n| ol       | style, type        | 1, a, A list types only                |\n| p        | style              |\n| pre      | style              |\n| span     | style              |\n| strong   | style              |\n| u        | style              |\n| ul       | style              | bullet glyphs only                     |\n\n## License\n\n[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fbauripalash%2Ftkhtmlview.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fbauripalash%2Ftkhtmlview?ref=badge_large)\n',
    'author': 'Palash Bauri',
    'author_email': 'palashbauri1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
