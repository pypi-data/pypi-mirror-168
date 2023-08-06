# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sylloge']

package_data = \
{'': ['*']}

install_requires = \
['moviegraphbenchmark>=1.0.1,<2.0.0',
 'pandas>=1.1.5,<2.0.0',
 'pystow>=0.4.6,<0.5.0']

extras_require = \
{'docs': ['Sphinx>=5.0.0,<6.0.0',
          'insegel>=1.3.1,<2.0.0',
          'sphinx-automodapi>=0.14.1,<0.15.0',
          'sphinx-autodoc-typehints>=1.19.2,<2.0.0']}

setup_kwargs = {
    'name': 'sylloge',
    'version': '0.1.0',
    'description': 'Small library to simplify collecting and loading of entity alignment benchmark datasets',
    'long_description': '<p align="center">\n<img src="https://github.com/dobraczka/sylloge/raw/main/docs/logo.png" alt="sylloge logo", width=200/>\n</p>\n\n<h2 align="center">sylloge</h2>\n\n<p align="center">\n<a href="https://github.com/dobraczka/sylloge/actions/workflows/main.yml"><img alt="Actions Status" src="https://github.com/dobraczka/sylloge/actions/workflows/main.yml/badge.svg?branch=main"></a>\n<a href=\'https://sylloge.readthedocs.io/en/latest/?badge=latest\'><img src=\'https://readthedocs.org/projects/sylloge/badge/?version=latest\' alt=\'Documentation Status\' /></a>\n<a href="https://pypi.org/project/sylloge"/><img alt="Stable python versions" src="https://img.shields.io/pypi/pyversions/sylloge"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\nThis simple library aims to collect entity-alignment benchmark datasets and make them easily available.\n\nUsage\n=====\n```\n>>> from sylloge import OpenEA\n>>> ds = OpenEA()\n>>> ds\nOpenEA(graph_pair=D_W, size=15K, version=V1, rel_triples_left=38265, rel_triples_right=42746, attr_triples_left=52134, attr_triples_right=138246, ent_links=15000, folds=5)\n>>> ds.rel_triples_right.head()\n                                       head                             relation                                    tail\n0   http://www.wikidata.org/entity/Q6176218   http://www.wikidata.org/entity/P27     http://www.wikidata.org/entity/Q145\n1   http://www.wikidata.org/entity/Q212675  http://www.wikidata.org/entity/P161  http://www.wikidata.org/entity/Q446064\n2   http://www.wikidata.org/entity/Q13512243  http://www.wikidata.org/entity/P840      http://www.wikidata.org/entity/Q84\n3   http://www.wikidata.org/entity/Q2268591   http://www.wikidata.org/entity/P31   http://www.wikidata.org/entity/Q11424\n4   http://www.wikidata.org/entity/Q11300470  http://www.wikidata.org/entity/P178  http://www.wikidata.org/entity/Q170420\n>>> ds.attr_triples_left.head()\n                                  head                                          relation                                               tail\n0  http://dbpedia.org/resource/E534644                http://dbpedia.org/ontology/imdbId                                            0044475\n1  http://dbpedia.org/resource/E340590               http://dbpedia.org/ontology/runtime  6480.0^^<http://www.w3.org/2001/XMLSchema#double>\n2  http://dbpedia.org/resource/E840454  http://dbpedia.org/ontology/activeYearsStartYear     1948^^<http://www.w3.org/2001/XMLSchema#gYear>\n3  http://dbpedia.org/resource/E971710       http://purl.org/dc/elements/1.1/description                          English singer-songwriter\n4  http://dbpedia.org/resource/E022831       http://dbpedia.org/ontology/militaryCommand                     Commandant of the Marine Corps\n>>> ds.ent_links.head()\n                                  left                                    right\n0  http://dbpedia.org/resource/E123186    http://www.wikidata.org/entity/Q21197\n1  http://dbpedia.org/resource/E228902  http://www.wikidata.org/entity/Q5909974\n2  http://dbpedia.org/resource/E718575   http://www.wikidata.org/entity/Q707008\n3  http://dbpedia.org/resource/E469216  http://www.wikidata.org/entity/Q1471945\n4  http://dbpedia.org/resource/E649433  http://www.wikidata.org/entity/Q1198381\n```\n\nInstallation\n============\n```bash\npip install sylloge \n```\n\nDatasets\n========\n| Dataset family name | Year | # of Datasets | Sources | Authors | Reference |\n|:--------------------|:----:|:-------------:|:-------:|:--------|:----------|\n| OpenEA | 2020 | 16 | DBpedia, Yago, Wikidata | Zun, S. et. al. | [Paper](http://www.vldb.org/pvldb/vol13/p2326-sun.pdf) |\n| MovieGraphBenchmark | 2022 | 3 | IMDB, TMDB, TheTVDB | Obraczka, D. et. al. | [Paper](http://ceur-ws.org/Vol-2873/paper8.pdf) |\n',
    'author': 'Daniel Obraczka',
    'author_email': 'obraczka@informatik.uni-leipzig.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dobraczka/sylloge',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
