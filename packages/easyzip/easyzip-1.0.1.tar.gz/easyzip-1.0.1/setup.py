import setuptools

# INSTALLATION
# pip3 install .

# BUILD
# python3 setup.py sdist bdist_wheel

# UPLOAD
# twine upload dist/*

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name                          = 'easyzip',
	version                       = '1.0.1',
	author                        = "Blind Holmes",
	author_email                  = "hewenhan@gmail.com",
	description                   = "Easy zip file or directory with password",
	long_description              = long_description,
	long_description_content_type = "text/markdown",
	url                           = "https://github.com/hewenhan/easyzip",
	packages                      = setuptools.find_packages(),
	install_requires              = ['pyminizip'],
	classifiers                   = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	]
)
