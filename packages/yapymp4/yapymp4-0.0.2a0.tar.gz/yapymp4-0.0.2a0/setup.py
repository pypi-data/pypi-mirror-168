import setuptools
import re
import os


VERSION=os.environ['YAPY_MP4_VERSION']
def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/__init__.py').read())
    return result.group(1)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yapymp4", # Replace with your own username
    version=VERSION,
    author="Charilaos Mylonas",
    author_email="mylonas.charilaos@gmail.com",
    description="Implementation of a parser for MP4 in pure python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mylonasc/yapyMP4.git",
    packages=setuptools.find_packages(),
    package_data ={'':['assets/html_css/*css','assets/html_css/*js']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
