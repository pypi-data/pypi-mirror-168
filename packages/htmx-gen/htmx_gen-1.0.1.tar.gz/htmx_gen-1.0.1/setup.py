# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['htmx_gen']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'htmx-gen',
    'version': '1.0.1',
    'description': 'Generate HTML conveniently and efficiently',
    'long_description': 'This module contains functions to generate HTML conveniently and efficiently.\n\nIt is an alternative to templating engines, like Jinja,\nfor use with, e.g., `htmx <https://htmx.org/>`__.\n\nPros:\n\n- use familiar python syntax\n\n- use efficient concatenation techniques (`join`, see `here <https://python.plainenglish.io/concatenating-strings-efficiently-in-python-9bfc8e8d6f6e>`__)\n\n- optional automatic indentation\n\nCons:\n\n- the name of some tag attributes is changed (e.g., ``class_`` instead of ``class``, due to Python parser)\n\n- possible conflicts of function names in your code base\n\n\nInstallation\n------------\n``pip install htmx_gen`` or copy the (single) source file in your project.\n\nDon\'t forget to `add a star on GitHub <https://github.com/pcarbonn/htmx_gen>`_ ! Thanks.\n\n\nTutorial:\n---------\n\n>>> from htmx_gen import *\n\nA tag is created by calling a function of the corresponding name,\nand rendered using ``render``:\n\n>>> print(render(p("text")))\n<p>text</p>\n\n\nTag attributes are specified using named arguments:\n\n>>> print(render(br(id="1")))\n<br id="1">\n\n>>> print(render(br(id=None)))\n<br>\n\n>>> print(render(ul(li("text", selected=True))))\n<ul><li selected>text</li></ul>\n\n>>> print(render(ul(li("text", selected=False))))\n<ul><li>text</li></ul>\n\n\nSome tag attributes are changed: you must add ``_`` to tag (or attribute) names\nconflicting with Python reserved names, (e.g. ``class_`` instead of ``class``),\nand you must use ``_`` instead of ``-`` in attribute names.\n\n>>> print(render(p("text", class_="s12", hx_get="url")))\n<p class="s12" hx-get="url">text</p>\n\n>>> print(render(button("Click me", hx_post="/clicked", hx_swap="outerHTML")))\n<button hx-post="/clicked" hx-swap="outerHTML">Click me</button>\n\n\nThe innerHTML can be a list:\n\n>>> print(render(div(["text", span("item 1"), span("item 2")])))\n<div>text<span>item 1</span><span>item 2</span></div>\n\nThe innerHTML can also be a list of lists:\n\n>>> print(render(div(["text", [span(f"item {i}") for i in [1,2]]])))\n<div>text<span>item 1</span><span>item 2</span></div>\n\n\nThe innerHTML can also be specified using the ``i`` parameter,\nafter the other attributes, to match the order of rendering:\n\n>>> print(render(ul(class_="s12", i=[\n...                 li("item 1"),\n...                 li("item 2")]\n...      )))\n<ul class="s12"><li>item 1</li><li>item 2</li></ul>\n\n\nWhen debugging your code, you can set global variable ``indent`` to ``True``\n(or call ``indent_it(True)``) to obtain HTML with tag indentation, e.g.,\n\n>>> indent_it(True); print(render(div(class_="s12", i=["text", span("item 1"), span("item 2")])))\n<div class="s12">\n  text\n  <span>\n    item 1\n  </span>\n  <span>\n    item 2\n  </span>\n</div>\n<BLANKLINE>\n',
    'author': 'Pierre',
    'author_email': 'pierre.carbonnelle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pcarbonn/htmx_gen',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
