# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opensearchorm']

package_data = \
{'': ['*']}

install_requires = \
['opensearch-py>=2.0.0,<3.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pytz>=2022.2.1,<2023.0.0']

setup_kwargs = {
    'name': 'opensearch-orm',
    'version': '0.1.0',
    'description': '',
    'long_description': "# OpenSearch ORM\n`opensearch-orm` is a high-level OpenSearch ORM for Python. The query syntax is similar to django-orm.\n\nMay be compatible with Elasticsearch, depending on opensearch-py.\n\n\n# Installation\n``` bash\npip install opensearchorm\n```\n\n\n# Getting Started\n\nFirst, define your document model with indexing pattern.\n``` python\nfrom opensearchorm import SearchSession, BaseModel\n\n\nclass UserLog(BaseModel):\n    __index__ = 'user_access_log-*'\n\n    method: str\n    path: str\n    remote_ip: str\n    created: datetime\n```\n\n\nYou can use django-like syntax or typed query expressions together.\n## filter\n``` python\n# {'bool': {'must_not': [], 'should': [], 'filter': [{'range': {'created': {'gte': '2022-09-01'}}}, {'match_phrase': {'remote_ip': '127.0.0.1'}}]}}        \nwith SearchSession() as session:\n    result = (\n        session.select(UserLog)\n        .filter(created__gte='2022-09-01', remote_ip='127.0.0.1')\n        .fetch()\n    )\n    print(result)\n\n    # equals to\n    result = (\n        session.select(UserLog)\n        .filter(Range('created', date(2022, 9, 1)), remote_ip='127.0.0.1')\n        .fetch()\n    )\n```\n## contains\n``` python\n# {'bool': {'must_not': [], 'should': [], 'filter': [{'bool': {'should': [{'match_phrase': {'method': 'GET'}}, {'match_phrase': {'method': 'POST'}}], 'minimum_should_match': 1}}]}}      \nwith SearchSession() as session:\n    result = (\n        session.select(UserLog)\n        .filter(method__contains=['GET', 'POST'])\n        .fetch()\n    )\n    print(result)\n\n    # equals to\n    result = (\n        session.select(UserLog)\n        .filter(Contains('method', ['GET', 'POST']))\n        .fetch()\n    )\n```\n\n## exclude\n``` python\n{'bool': {'must_not': [{'match_phrase': {'method': 'get'}}, {'match_phrase': {'path': '/login'}}], 'should': [], 'filter': []}}\nwith SearchSession() as session:\n    result = (\n        session.select(UserLog)\n        .exclude(method='get', path='/login')\n        .fetch()\n    )\n    print(result)\n```\n\n\n## paginate\n``` python\nwith SearchSession() as session:\n    result = (\n        session.select(UserLog)\n        .filter(method='get')\n        .limit(100)\n        .offset(100)\n        .fetch()\n    )\n    print(result)\n```\n\n## aggregations\ngroup by path and count unique remote_ip\n``` python\nwith SearchSession() as session:\n    result = (\n        session.select(UserLog)\n        .aggregate(Terms('path').nested(Cardinality('remote_ip')))\n    )\n    print(result)\n    # result -> {'path': 1, 'path2': 2}\n```",
    'author': 'yim7',
    'author_email': 'yimchiu7@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
