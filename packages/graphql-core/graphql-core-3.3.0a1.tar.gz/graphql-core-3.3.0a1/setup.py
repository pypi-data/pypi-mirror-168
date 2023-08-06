# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['docs',
 'graphql',
 'graphql.error',
 'graphql.execution',
 'graphql.language',
 'graphql.pyutils',
 'graphql.type',
 'graphql.utilities',
 'graphql.validation',
 'graphql.validation.rules',
 'graphql.validation.rules.custom',
 'tests',
 'tests.benchmarks',
 'tests.error',
 'tests.execution',
 'tests.fixtures',
 'tests.language',
 'tests.pyutils',
 'tests.type',
 'tests.utilities',
 'tests.utils',
 'tests.validation']

package_data = \
{'': ['*'], 'docs': ['modules/*', 'usage/*']}

modules = \
['.bumpversion',
 '.editorconfig',
 '.flake8',
 '.readthedocs',
 'poetry',
 'tox',
 'CODEOWNERS',
 'SECURITY']
extras_require = \
{':python_version < "3.8"': ['typing-extensions>=4.3,<5.0']}

setup_kwargs = {
    'name': 'graphql-core',
    'version': '3.3.0a1',
    'description': 'GraphQL-core is a Python port of GraphQL.js,the JavaScript reference implementation for GraphQL.',
    'long_description': '# GraphQL-core 3\n\nGraphQL-core 3 is a Python 3.6+ port of [GraphQL.js](https://github.com/graphql/graphql-js),\nthe JavaScript reference implementation for [GraphQL](https://graphql.org/),\na query language for APIs created by Facebook.\n\n[![PyPI version](https://badge.fury.io/py/graphql-core.svg)](https://badge.fury.io/py/graphql-core)\n[![Documentation Status](https://readthedocs.org/projects/graphql-core-3/badge/)](https://graphql-core-3.readthedocs.io)\n![Test Status](https://github.com/graphql-python/graphql-core/actions/workflows/test.yml/badge.svg)\n![Lint Status](https://github.com/graphql-python/graphql-core/actions/workflows/lint.yml/badge.svg)\n[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nAn extensive test suite with over 2300 unit tests and 100% coverage comprises a\nreplication of the complete test suite of GraphQL.js, making sure this port is\nreliable and compatible with GraphQL.js.\n\nThe current stable version 3.2.3 of GraphQL-core is up-to-date with GraphQL.js version 16.6.0.\n\nYou can also try out the latest alpha version 3.3.0a1 of GraphQL-core that is up-to-date with GraphQL.js version 17.0.0a1.\nPlease note that this new minor version of GraphQL-core does not support Python 3.7 anymore.\n\nNote that for various reasons, GraphQL-core does not use SemVer like GraphQL.js. Changes in the major version of GraphQL.js are reflected in the minor version of GraphQL-core instead. This means there can be breaking changes in the API when the minor version changes, and only patch releases are fully backward compatible. Therefore, we recommend something like `=~ 3.2.0` as version specifier when including GraphQL-core as a dependency.\n\n\n## Documentation\n\nA more detailed documentation for GraphQL-core 3 can be found at\n[graphql-core-3.readthedocs.io](https://graphql-core-3.readthedocs.io/).\n\nThe documentation for GraphQL.js can be found at [graphql.org/graphql-js/](https://graphql.org/graphql-js/).\n\nThe documentation for GraphQL itself can be found at [graphql.org](https://graphql.org/).\n\nThere will be also [blog articles](https://cito.github.io/tags/graphql/) with more usage\nexamples.\n\n\n## Getting started\n\nA general overview of GraphQL is available in the\n[README](https://github.com/graphql/graphql-spec/blob/main/README.md) for the\n[Specification for GraphQL](https://github.com/graphql/graphql-spec). That overview\ndescribes a simple set of GraphQL examples that exist as [tests](tests) in this\nrepository. A good way to get started with this repository is to walk through that\nREADME and the corresponding tests in parallel.\n\n\n## Installation\n\nGraphQL-core 3 can be installed from PyPI using the built-in pip command:\n\n    python -m pip install graphql-core\n\nYou can also use [poetry](https://github.com/python-poetry/poetry) for installation in a\nvirtual environment:\n\n    poetry install\n\n\n## Usage\n\nGraphQL-core provides two important capabilities: building a type schema and\nserving queries against that type schema.\n\nFirst, build a GraphQL type schema which maps to your codebase:\n\n```python\nfrom graphql import (\n    GraphQLSchema, GraphQLObjectType, GraphQLField, GraphQLString)\n\nschema = GraphQLSchema(\n    query=GraphQLObjectType(\n        name=\'RootQueryType\',\n        fields={\n            \'hello\': GraphQLField(\n                GraphQLString,\n                resolve=lambda obj, info: \'world\')\n        }))\n```\n\nThis defines a simple schema, with one type and one field, that resolves to a fixed\nvalue. The `resolve` function can return a value, a co-routine object or a list of\nthese. It takes two positional arguments; the first one provides the root or the\nresolved parent field, the second one provides a `GraphQLResolveInfo` object which\ncontains information about the execution state of the query, including a `context`\nattribute holding per-request state such as authentication information or database\nsession. Any GraphQL arguments are passed to the `resolve` functions as individual\nkeyword arguments.\n\nNote that the signature of the resolver functions is a bit different in GraphQL.js,\nwhere the context is passed separately and arguments are passed as a single object.\nAlso note that GraphQL fields must be passed as a `GraphQLField` object explicitly.\nSimilarly, GraphQL arguments must be passed as `GraphQLArgument` objects.\n\nA more complex example is included in the top-level [tests](tests) directory.\n\nThen, serve the result of a query against that type schema.\n\n```python\nfrom graphql import graphql_sync\n\nsource = \'{ hello }\'\n\nprint(graphql_sync(schema, source))\n```\n\nThis runs a query fetching the one field defined, and then prints the result:\n\n```python\nExecutionResult(data={\'hello\': \'world\'}, errors=None)\n```\n\nThe `graphql_sync` function will first ensure the query is syntactically and\nsemantically valid before executing it, reporting errors otherwise.\n\n```python\nfrom graphql import graphql_sync\n\nsource = \'{ BoyHowdy }\'\n\nprint(graphql_sync(schema, source))\n```\n\nBecause we queried a non-existing field, we will get the following result:\n\n```python\nExecutionResult(data=None, errors=[GraphQLError(\n    "Cannot query field \'BoyHowdy\' on type \'RootQueryType\'.",\n    locations=[SourceLocation(line=1, column=3)])])\n```\n\nThe `graphql_sync` function assumes that all resolvers return values synchronously. By\nusing coroutines as resolvers, you can also create results in an asynchronous fashion\nwith the `graphql` function.\n\n```python\nimport asyncio\nfrom graphql import (\n    graphql, GraphQLSchema, GraphQLObjectType, GraphQLField, GraphQLString)\n\n\nasync def resolve_hello(obj, info):\n    await asyncio.sleep(3)\n    return \'world\'\n\nschema = GraphQLSchema(\n    query=GraphQLObjectType(\n        name=\'RootQueryType\',\n        fields={\n            \'hello\': GraphQLField(\n                GraphQLString,\n                resolve=resolve_hello)\n        }))\n\n\nasync def main():\n    query = \'{ hello }\'\n    print(\'Fetching the result...\')\n    result = await graphql(schema, query)\n    print(result)\n\n\nasyncio.run(main())\n```\n\n\n## Goals and restrictions\n\nGraphQL-core tries to reproduce the code of the reference implementation GraphQL.js\nin Python as closely as possible and to stay up-to-date with the latest development of\nGraphQL.js.\n\nGraphQL-core 3 (formerly known as GraphQL-core-next) has been created as a modern\nalternative to [GraphQL-core 2](https://github.com/graphql-python/graphql-core-legacy),\na prior work by Syrus Akbary, based on an older version of GraphQL.js and also\ntargeting older Python versions. Some parts of GraphQL-core 3 have been inspired by\nGraphQL-core 2 or directly taken over with only slight modifications, but most of the\ncode has been re-implemented from scratch, replicating the latest code in GraphQL.js\nvery closely and adding type hints for Python.\n\nDesign goals for the GraphQL-core 3 library were:\n\n* to be a simple, cruft-free, state-of-the-art GraphQL implementation for current\n  Python versions\n* to be very close to the GraphQL.js reference implementation, while still providing\n  a Pythonic API and code style\n* to make extensive use of Python type hints, similar to how GraphQL.js used Flow\n  (and is now using TypeScript)\n* to use [black](https://github.com/ambv/black) to achieve a consistent code style\n  while saving time and mental energy for more important matters\n* to replicate the complete Mocha-based test suite of GraphQL.js\n  using [pytest](https://docs.pytest.org/)\n  with [pytest-describe](https://pypi.org/project/pytest-describe/)\n\nSome restrictions (mostly in line with the design goals):\n\n* requires Python 3.6 or newer\n* does not support some already deprecated methods and options of GraphQL.js\n* supports asynchronous operations only via async.io\n  (does not support the additional executors in GraphQL-core)\n\n\n## Integration with other libraries and roadmap\n\n* [Graphene](http://graphene-python.org/) is a more high-level framework for building\n  GraphQL APIs in Python, and there is already a whole ecosystem of libraries, server\n  integrations and tools built on top of Graphene. Most of this Graphene ecosystem has\n  also been created by Syrus Akbary, who meanwhile has handed over the maintenance\n  and future development to members of the GraphQL-Python community.\n\n  The current version 2 of Graphene is using Graphql-core 2 as core library for much of\n  the heavy lifting. Note that Graphene 2 is not compatible with GraphQL-core 3.\n  The  new version 3 of Graphene will use GraphQL-core 3 instead of GraphQL-core 2.\n\n* [Ariadne](https://github.com/mirumee/ariadne) is a Python library for implementing\n  GraphQL servers using schema-first approach created by Mirumee Software.\n\n  Ariadne is already using GraphQL-core 3 as its GraphQL implementation.\n\n* [Strawberry](https://github.com/strawberry-graphql/strawberry), created by Patrick\n  Arminio, is a new GraphQL library for Python 3, inspired by dataclasses,\n  that is also using GraphQL-core 3 as underpinning.\n\n\n## Changelog\n\nChanges are tracked as\n[GitHub releases](https://github.com/graphql-python/graphql-core/releases).\n\n\n## Credits and history\n\nThe GraphQL-core 3 library\n* has been created and is maintained by Christoph Zwerschke\n* uses ideas and code from GraphQL-core 2, a prior work by Syrus Akbary\n* is a Python port of GraphQL.js which has been developed by Lee Byron and others\n  at Facebook, Inc. and is now maintained\n  by the [GraphQL foundation](https://gql.foundation/join/)\n\nPlease watch the recording of Lee Byron\'s short keynote on the\n[history of GraphQL](https://www.youtube.com/watch?v=VjHWkBr3tjI)\nat the open source leadership summit 2019 to better understand\nhow and why GraphQL was created at Facebook and then became open sourced\nand ported to many different programming languages.\n\n\n## License\n\nGraphQL-core 3 is\n[MIT-licensed](./LICENSE),\njust like GraphQL.js.\n',
    'author': 'Christoph Zwerschke',
    'author_email': 'cito@online.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/graphql-python/graphql-core',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
