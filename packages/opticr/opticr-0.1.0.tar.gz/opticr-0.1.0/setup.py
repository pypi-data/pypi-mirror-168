# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opticr', 'opticr.ocr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'opticr',
    'version': '0.1.0',
    'description': 'expose a single interface and API to few OCR tools',
    'long_description': '# opticr\n\nPython library to expose a single interface and API to few OCR tools (google vision, Textract)\n\n## Install\n### With pip\n\n``` shell\npip install opticr\n```\n\n### With poetry\n\n``` shell\npoetry add opticr\n```\n\nor to get the latest \'dangerous\' version\n\n```\npoetry add  git+https://github.com/lzayep/opticr@main\n```\n\n## Usage\n\n``` python\nfrom opticr import OpticR\n\nocr = OpticR("textract")\npathtofile = "test/contract.pdf\npages: list[str] = ocr.get_pages(pathtofile)\n\n```\n\nWith google-vision:\n\n``` python\nfrom opticr import OpticR\n\nocr = OpticR("google-vision", options={"google-vision": {"auth": {"token": ""}}})\n\n# file could come from an URL\npathtofile = "https://example.com/contract.pdf\npages: list[str] = ocr.get_pages(pathtofile)\n\n```\n\nCache the result, if the file as already been OCR return immediatly the previous result.\nResult are stored temporarly in the local storage or shared storage such as Redis.\n``` python\nfrom opticr import OpticR\n\nocr = OpticR("textract", options={"cache":\n                         {"backend": "redis", redis: "redis://"}}\n\n# file could come from an URL\npathtofile = "https://example.com/contract.pdf\npages: list[str] = ocr.get_pages(pathtofile, cache=True)\n\n```\n',
    'author': 'lzayep',
    'author_email': 'ec@lza.sh',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
