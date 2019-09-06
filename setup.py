from setuptools import setup
setup(name='Dictableobject',
	version='1.1.1',
	description='A menagerie of base classes to make objects that can be written as dicts.',
	url='https://www.github.com/pmp47/Dictableobject',
	author='pmp47',
	author_email='phil@zeural.com',
	license='MIT',
	packages=['dictableobject'],
	install_requires=['Security==1.1.15'],
	zip_safe=False,
	include_package_data=True,
	python_requires='>=3.6',

	package_data={'': ['data/*.*']}
)
