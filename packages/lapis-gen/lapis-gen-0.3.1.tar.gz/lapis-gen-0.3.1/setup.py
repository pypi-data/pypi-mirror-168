# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lapis',
 'lapis.openapi',
 'lapis.render',
 'lapis.render.elems',
 'lapis.render.templates']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'black>=22.8.0,<23.0.0',
 'inflection>=0.5.1,<0.6.0',
 'jsonpatch>=1.32,<2.0',
 'lapis-client-base>=0.2.2,<0.3.0',
 'pydantic[email]>=1.9.2,<2.0.0',
 'python-mimeparse>=1.6.0,<2.0.0',
 'tomlkit>=0.11.4,<0.12.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['lapis = lapis.__main__:start']}

setup_kwargs = {
    'name': 'lapis-gen',
    'version': '0.3.1',
    'description': 'Python API client generator',
    'long_description': "# Lapis - Python OpenAPI client generator\n\nGenerate OpenAPI 3.0.3 client code that is easy to understand and debug.\n\nLeverages [Pydantic](https://github.com/pydantic/pydantic) as the base classes\nand [httpx](https://github.com/encode/httpx) as the HTTP client.\n\n## Usage\n\nlapis [--errata path] spec_file target_dir root_package\n\nLapis will create target_dir, all necessary directories and pyproject.toml if they don't exist.\n\nGenerated files will be placed in <target_dir>/gen/<root_package>\n\nErrata is a JSON Patch file in JSON or YAML format; it's applied to the spec before any other processing.\n\n## Supported OpenAPI features\n\n- Parameter names: operation parameters are uniquely identified by their name the value of an `in` attribute. It is possible to have parameter named `param` in all of path, query, cookies and headers.\n  \n  Lapis uses Hungarian notation for method parameter names.\n- Enums: [TODO] there's no limitation that enum schema cannot be an object or an array.\n\n  Enums might need two python classes - a subclass of `enum.Enum` and the schema class.\n- oneOf: maps to typing.Union\n- AllOf: [TODO] maps to a separate class that uses all the schemas as superclasses.\n- AnyOf: [TODO] maps to similar class as in case of AllOf, all fields should be non-required and the object should validate against at least one of superclasses.\n- Recursive references between schemas: supported.\n- References to other schemas: unsupported.\n- Read- and write-only attributes: [TODO] Read-only attributes are considered non-existent when the object is validated before being sent to the server.\n\n## Broken and incomplete API specifications\n\n- errata: use errata to update the specification document in cases where actual data doesn't match it, and the service provider is reluctant or slow to update it.\n\nTODO: pre- and postprocessing of API specification (dict- and pydantic-based models) with python code, errata (jsonpatch), etc\n\n## Backwards compatibility\n\nOnce stable, Lapis should generate code that is backwards compatible as long as the API specification is too. The following rules are used to ensure that.\n\nNames of interface elements (public functions, classes and methods) are fully deterministic and are derived only from their source elements and, in some cases, their parents.\nFor example, schemas of the same name are either placed in separate modules, or their names have the parent element name prepended. \n\nEach operation must have operationId which is used to create a unique package for its models.\n\nThe structure of the API specification is roughly reflected in the generated code.\nEach schema under #/components/schemas together with all inline parameter schemas will become a single module in `<your_package>.components.schemas`.\nEach operation must define `operationId` which will be used as a sub-package name for the module containing its all inline schemas. Operation packages will be placed under `<your_package>.paths`\n\n",
    'author': 'Raphael Krupinski',
    'author_email': 'rafalkrupinski@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lapis-project/lapis',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
