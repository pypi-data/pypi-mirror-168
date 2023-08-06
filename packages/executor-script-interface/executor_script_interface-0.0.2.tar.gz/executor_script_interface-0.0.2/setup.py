from setuptools import setup, find_packages
from executor_script_interface import version

# Setting up
setup(
    name="executor_script_interface",
    version="{v[0]}.{v[1]}.{v[2]}".format(v=version.__version__.split('.')),
    author="Nilar Software Engineering",
    url="https://www.nilar.com",
    author_email="softwarengineering@nilar.com",
    description="Scripting interface for NilarTestExecutor",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    packages=find_packages(),
    python_requires = ">=3.5",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "License :: OSI Approved :: MIT License"
    ]
)