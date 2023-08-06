# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['holisticai',
 'holisticai.bias',
 'holisticai.bias.metrics',
 'holisticai.bias.mitigation',
 'holisticai.bias.mitigation.inprocessing',
 'holisticai.bias.mitigation.inprocessing.commons',
 'holisticai.bias.mitigation.inprocessing.exponentiated_gradient',
 'holisticai.bias.mitigation.inprocessing.grid_search',
 'holisticai.bias.mitigation.postprocessing',
 'holisticai.bias.mitigation.preprocessing',
 'holisticai.bias.plots',
 'holisticai.datasets',
 'holisticai.pipeline',
 'holisticai.utils',
 'holisticai.utils.transformers',
 'holisticai.utils.transformers.bias']

package_data = \
{'': ['*']}

install_requires = \
['scikit-learn>=1.0.2', 'seaborn>=0.11.2']

setup_kwargs = {
    'name': 'holisticai',
    'version': '0.1.1',
    'description': 'Holistic AI Library',
    'long_description': '# holisticai\n\n> The Holistic AI library is an open-source tool to assess and improve the trustworthiness of AI systems.\n',
    'author': 'Research Team',
    'author_email': 'None',
    'maintainer': 'Research Team',
    'maintainer_email': 'researchteam@holisticai.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
