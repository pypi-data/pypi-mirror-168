# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schema_classification',
 'schema_classification.bp',
 'schema_classification.dmo',
 'schema_classification.dto',
 'schema_classification.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock']

setup_kwargs = {
    'name': 'schema-classification',
    'version': '0.1.4',
    'description': 'Perform Intent Classification using an External Schema',
    'long_description': '# schema-classification\nThis microservice performs the classification of parse results\n\n## Usage\nThe input format looks like this\n```python\ninput_tokens = [\n    {\n        "normal": "my",\n    },\n    {\n        "normal": "late",\n    },\n    {\n        "normal": "transport",\n    },\n    {\n        "normal": "late_transport",\n        "swaps": {\n            "canon": "late_transport",\n            "type": "chitchat"\n        }\n    },\n]\n```\n\nCalling the service looks like this\n```python\nfrom schema_classification import classify\n\nabsolute_path = os.path.normpath(\n    os.path.join(os.getcwd(), \'resources/testing\',\n                    \'test-intents-0.1.0.yaml\'))\n\nsvcresult = classify(\n    absolute_path=absolute_path,\n    input_tokens=input_tokens)\n```\n\nThe output from this call looks like\n```python\n{\n    \'result\': [{\n        \'classification\': \'Late_Transport\',\n        \'confidence\': 99 }],\n    \'tokens\': {\n        \'late\': \'\',\n        \'late_transport\': \'chitchat\',\n        \'my\': \'\',\n        \'transport\': \'\'}\n}\n```\n\n\n## Classification via Mapping\nClassification of Unstructured Text is a mapping exercise\n\nThe mapping is composed of these elements\n1. Include One Of\n2. Include All Of\n3. Exclude One Of\n4. Exclude All Of\n\nThe classifier will map extracted entities from unstructured text using the listed elements.\n\nfor example,\n\n```yaml\nTEST_INTENT\n  - include_one_of:\n    - alpha\n    - apple\n  - include_all_of:\n    - beta\n    - gamma\n  - exclude_one_of:\n    - delta\n  - exclude_all_of:\n    - epsilon\n    - digamma\n```\n\nThis intent will be selected if the set of extracted entities has either `alpha` or `apple` and has both `(beta, gamma)`. The intent will be discarded if `delta` occurs or if both `(epsilon, digamma)` occur.\n\nIn python, everything can be loaded into a native set structure and use native operations like `difference`, `intersection`, `union`, and `symmetric difference`.\n\nBecause all set operations are native (underlying C modules), it\'s extremely fast to find an accurate classification.\n\nThe system adds more smarts by figuring out what to do if the rule states `delta` is excluded, and a descendant of `delta` is present.\n\nOr if `alpha` should be included and a sibling or child of `alpha` is present, etc.\n\nIn this case, I usually rely on a heuristic to boost or lower confidence and tweak that overtime to get a good result.',
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': 'Craig Trim',
    'maintainer_email': 'craigtrim@gmail.com',
    'url': 'https://github.com/craigtrim/spacy-token-parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.5',
}


setup(**setup_kwargs)
