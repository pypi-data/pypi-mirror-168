import codecs, os
from setuptools import setup, find_packages

package_path = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(package_path, "README.md"), encoding="utf-8") as f:
    detailed_desc = "\n" + f.read()

version = "0.0.1"
description = "Easily make macros in Python!"

setup(
    name="easymacro",
    version=version,
    author="Wurgo, Languste27",
    author_email="<wurgoalt@gmail.com>",
    description=description,
    long_description_content_type="text/markdown",
    long_description=detailed_desc,
    packages=find_packages(),
    install_requires=["pywin32"],
    keywords=["python", "macro", "windows", "mouse", "keyboard", "input"],
    classifiers=[]
)
