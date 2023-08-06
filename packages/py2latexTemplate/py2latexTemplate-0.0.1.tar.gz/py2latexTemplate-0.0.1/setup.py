from setuptools import setup
			
with open('README.md', 'r') as fh:
	long_description = fh.read()

setup(
	name="py2latexTemplate",
	version="0.0.1",
	author="Gabrielle Ohlson",
	description="Code for producing LaTeX files with python scripts (heavily dependent on sympy module); makes it simpler to format elegantly and include python math/code blocks in your LaTeX.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/gabrielle-ohlson/py2latexTemplate",
	packages=['py2latexTemplate'],
	install_requires=['sympy']
)