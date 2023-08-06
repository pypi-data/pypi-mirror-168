# Building and maintaing a python package for DESC

### Creating a python package

Start of by going to the DESC github [repository creation
page](https://github.com/organizations/LSSTDESC/repositories/new) 

Pick sensible answers for the various questions and then click on the 
"Create repository" big green button.

Here are some sensible answers:

<img src="create_package.png" alt="Create Package" width="500"/>

Pro-tip: naviagate to the page for your newly created repository, e.g., 
[eac-test](https://github.com/LSSTDESC/eac-test) and click on the
"Code" pull down menu and click on the two little box next to the URL
to copy the URL to your clipboard.

<img src="get_code.png" alt="Get code" width="500"/>

Open a terminal on your computer and navigate to the place you want to
install the code, then clone the code.

	cd <somewhere>
	git clone https://github.com/LSSTDESC/<package>.git
	cd <package>


Make the basic package structure

	mkdir src
	mdkir src/<package> # This is where your code goes
	mkdir tests
	mkdir tests/<package> # This is where your tests go
	mkdir docs
	mkdir .github
	mkdir .github/workflows # This is where the github actions go 
	
	
Add the python packaging and configuration stuff, you can copy then
from this package to get started.

	pyproject.toml # required
	setup.py # required
	.flake8 # optional, useful if you want to use flake8 for code checking
	.github/workflows/main.yml # really useful for automated testing
	.github/workflows/pypi.yml # really useful to automatically releases
	
	
Edit pyproject.toml, you will need to do at minimum:

Change these fields in the '[project]' block:

	[project]
	name = "eac-test"
	description = "Test package to test packing"
	authors = [
		{ name = "Eric Charles", email = "echarles@slac.stanford.edu" }
	]
	dependencies = [
		"numpy",
	]

Change this field in the setup block to enable versioning based on the
git tag.

	[tool.setuptools_scm]
	write_to = "src/eac_test/_version.py"
	
If you have data you would like to package with the source code, add a
	block like this:
	
	[tool.setuptools.package-data]
	"eac_test.data" = ["*.txt"]


Point the coverage tools at the right code

	[tool.coverage.run]
	source = ["eac_test"]
	
	
	[tool.pytest.ini_options]
		addopts = [
		"--cov=eac_test",


