import re
from codecs import open
from os import path

from setuptools import setup

name = "kedro-rich"
here = path.abspath(path.dirname(__file__))

# get package version
package_name = name.replace("-", "_")
with open(path.join(here, package_name, "__init__.py"), encoding="utf-8") as f:
    version = re.search(r'__version__ = ["\']([^"\']+)', f.read()).group(1)

# get the dependencies and installs
with open("requirements.txt", "r", encoding="utf-8") as f:
    requires = [x.strip() for x in f if x.strip()]

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()

setup(
    name=name,
    version=version,
    description="Kedro-Rich",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Kedro",
    python_requires=">=3.6, <3.9",
    install_requires=requires,
    license="Apache Software License (Apache 2.0)",
    packages=["kedro_rich"],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "kedro.project_commands": ["kedro_rich_project = kedro_rich.rich_cli:commands"],
        "kedro.hooks" : ["kedro_rich_progress = kedro_rich.rich_progress_hooks:rich_hooks"],
        "kedro.init" : ["kedro_rich_init = kedro_rich.rich_init:start_up"]
    },
)
