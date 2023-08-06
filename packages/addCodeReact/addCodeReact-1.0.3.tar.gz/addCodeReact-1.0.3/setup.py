from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()

long_description = 'Package to add dynamic react components import code'

setup(
		name ='addCodeReact',
		version ='1.0.3',
		author ='Subha Sankari',
		author_email ='subhasankari1995@gmail.com',
		url ='https://github.com/subhasankari95/python_add_code_react',
		description ='Package for react code dynamically',
		long_description = long_description,
		long_description_content_type ="text/markdown",
		license ='MIT',
		packages = find_packages(),
		entry_points ={
			'console_scripts': [
				'addCode = myfunctionfolder.myfunction_click:main'
			]
		},
		classifiers =(
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
		),
		keywords ='python dynamic react code command line',
		install_requires = requirements,
		zip_safe = False
)
