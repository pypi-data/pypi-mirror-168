# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scistag',
 'scistag.addons',
 'scistag.cli',
 'scistag.common',
 'scistag.common.flask',
 'scistag.data',
 'scistag.datastag',
 'scistag.datastag4flask',
 'scistag.examples',
 'scistag.examples.imagestag',
 'scistag.examples.mediastag',
 'scistag.examples.slidestag',
 'scistag.filestag',
 'scistag.gitstag',
 'scistag.imagestag',
 'scistag.imagestag.filters',
 'scistag.mediastag',
 'scistag.remotestag',
 'scistag.slidestag',
 'scistag.slidestag4flask',
 'scistag.slidestag4kivy',
 'scistag.tests',
 'scistag.tests.common',
 'scistag.tests.datastag',
 'scistag.tests.datastag4flask',
 'scistag.tests.filestag',
 'scistag.tests.gitstag',
 'scistag.tests.imagestag',
 'scistag.tests.remotestag',
 'scistag.tests.slidestag',
 'scistag.tests.webstag',
 'scistag.third_party',
 'scistag.third_party.imgkit_fix',
 'scistag.webstag']

package_data = \
{'': ['*'], 'scistag.slidestag4flask': ['static/js/*', 'templates/*']}

install_requires = \
['CairoSVG>=2.5.2,<3.0.0',
 'abstract>=2022.7.10,<2023.0.0',
 'matplotlib>=3.5.2,<4.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pretty-html-table>=0.9.16,<0.10.0',
 'requests>=2.27.1,<3.0.0']

extras_require = \
{'docubuild': ['Sphinx>=5.1.1,<6.0.0',
               'sphinx-rtd-theme>=1.0.0,<2.0.0',
               'myst-parser>=0.18.0,<0.19.0',
               'sphinx_mdinclude>=0.5.2,<0.6.0',
               'anybadge>=1.14.0,<2.0.0',
               'sphinx-autodoc-typehints>=1.19.2,<2.0.0'],
 'flask': ['gunicorn>=20.1.0,<21.0.0', 'Flask>=2.1.2,<3.0.0'],
 'full': ['gunicorn>=20.1.0,<21.0.0',
          'Flask>=2.1.2,<3.0.0',
          'opencv-contrib-python>=4.5.4.60,<5.0.0.0',
          'moviepy>=1.0.3,<2.0.0',
          'Kivy>=2.1.0,<3.0.0',
          'imgkit==1.2.2'],
 'kivy': ['Kivy>=2.1.0,<3.0.0'],
 'opencv': ['opencv-contrib-python>=4.5.4.60,<5.0.0.0'],
 'slidestag': ['gunicorn>=20.1.0,<21.0.0',
               'Flask>=2.1.2,<3.0.0',
               'moviepy>=1.0.3,<2.0.0',
               'Kivy>=2.1.0,<3.0.0']}

setup_kwargs = {
    'name': 'scistag',
    'version': '0.0.2',
    'description': 'A stack of helpful libraries & applications for the rapid development of data driven solutions.',
    'long_description': "# SciStag\n\n### A stack of helpful libraries & applications for the rapid development of data driven solutions.\n\n```\n                                      (  (  )   (  )   )\n                                       `(  `(     )'  )'\n                                         `--(_   _)--'\n                                              \\-/\n                                             /oO \\\n                                            /..   \\\n                                            `--'.  \\              .             \n                                                 \\   `.__________/)\n```\n\n---\n\nBuild Status\n------------\n\n[![PyPi Version](https://img.shields.io/pypi/v/SciStag.svg)](https://pypi.python.org/pypi/SciStag)\n[![Documentation Status](https://readthedocs.org/projects/scistag/badge/?version=latest)](https://scistag.readthedocs.io/en/latest/?badge=latest)\n[![Coverage](https://coveralls.io/repos/github/SciStag/SciStag/badge.svg?branch=main)](https://coveralls.io/github/SciStag/SciStag)\n[![Pylint](docs/source/generated/pylint.svg)](https://coveralls.io/github/SciStag/SciStag)\n\n[![Ubuntu Unittests Status](https://github.com/scistag/scistag/workflows/Ubuntu%20Unittests/badge.svg)](https://github.com/scistag/scistag/actions?query=workflow%3A%22Ubuntu+Unittests%22)\n\n* SciStag is available on pypi: https://pypi.python.org/pypi/SciStag\n* The source is hosted on GitHub: https://github.com/SciStag/SciStag\n* The documentation is available on ReadTheDocs: https://scistag.readthedocs.io/\n\n---\n\nThis project is still under heavy development and in a very early stage - feel free to experiment with the modules and\nexamples which are already provided.\n\nThe goal of **SciStag** is to bundle the strengths of the many small, awesome Python technologies from OpenCV via Flask\nto Pandas and enable users to combine these libraries and build awesome data driven solutions with a minimum amount of\ncode.\n\nSciStag currently consists of the following so called **stags**:\n\n## SlideStag\n\n- Building interactive presentations in Python using the tools you love with a minimum of code.\n- SlideStag4Flask lets you host your interactive presentation as a browser application\n- SlideStag4Flutter lets you interact with your solution from an iPad (and from Android device soon too)\n- SlideStag4Kivy lets you integrate your solution into or host it via [Kivy](https://github.com/kivy/kivy).\n\n## ImageStag\n\n- Image analysis and modification made easy by combining the strengths of PILLOW, OpenCV and SKImage.\n\n## MediaStag\n\n- Easy integration of streaming media data such as videos into your solution.\n\n## DataStag\n\n- Low-latency inter-container and -process exchange of image and other binary data for Computer Vision and other data\n  intensive microservice architectures.\n\n## RemoteStag\n\n- Remote and asynchronous task execution - such as a neural network inference\n\n## WebStag\n\n* Helpful tools for accessing and processing web data\n\n## FileStag (planned)\n\n* Tools for handling local file and archive data.\n\n## CloudStag (planned)\n\n* Even easier access to cloud services of Azure, AWS & Co.\n\n... more details and examples to come ;-). Estimated official release: Summer 2023.\n\n---\n\n## Setup\n\nSciStag comes completely bundled with all required standard components.\n\n`pip install scistag[full]` or when using poetry `poetry add scistag[full]` and you are ready to go! :)\n\n### Optional components\n\n* ImageStag (and other components using ImageStag) support the rendering of HTML and websites via\n  [imgkit](https://pypi.org/project/imgkit/). If you do not use any of our pre-built Docker images please follow the\n  instructions on https://pypi.org/project/imgkit/ for your operating system if you want to make use of HTML rendering.\n\n## License\n\nCopyright (c) 2022-present Michael Ikemann.\n\nReleased under the terms of the **MIT License**.\n\n### Third-party data\n\nThe SciStag module on PyPi is bundled with the following data:\n\n* The [Roboto](https://fonts.google.com/specimen/Roboto) font - licensed and distributed under the terms of\n  the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).\n* The [Roboto Flex](https://github.com/googlefonts/roboto-flex) font - licensed under\n  the [SIL Open Font License 1.1](http://scripts.sil.org/cms/scripts/page.php?item_id=OFL_web)\n* The [JetBrains Mono](https://www.jetbrains.com/lp/mono/) font - licensed under\n  the [SIL Open Font License 1.1](http://scripts.sil.org/cms/scripts/page.php?item_id=OFL_web).\n* [Iconic font](https://github.com/Templarian/MaterialDesign-Webfont) by the Material Design Icons community covered\n  by [SIL Open Font License 1.1](http://scripts.sil.org/cms/scripts/page.php?item_id=OFL_web)\n* Emojis and country flags from the [Noto Emoji](https://github.com/googlefonts/noto-emoji) project. Tools and most\n  image resources are under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).\n    * Flag images under the public domain or otherwise exempt from copyright.\n* The emoji unicode character name mappings and details are based upon the unicode data files, Copyright © 1991-2022\n  Unicode, Inc, licensed under the terms of the [UNICODE, INC. LICENSE AGREEMENT](https://www.unicode.org/license.txt)\n\n### Third-party source code\n\n* Contains portions of code from [imkgit](https://github.com/jarrekk/imgkit), Copyright (C) 2016 Cory Dolphin, Olin\n  College, released under the terms of the **MIT License**.\n\n## Contributors\n\nSciStag is developed by Michael Ikemann / [@Alyxion](https://github.com/Alyxion). - Feel free to reach out to me\nvia [LinkedIn](https://www.linkedin.com/in/michael-ikemann/).\n\n",
    'author': 'Michael Ikemann',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/scistag/scistag',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
