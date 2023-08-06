from setuptools import setup, find_packages

str_version = '1.2.1'

setup(
	name='roo00kie-utils',
	version=str_version,
	author='roo00kie',
	author_email='roo00kie@roo00kie.com',
	url='https://github.com/Ro0kie/roo00kie-utils',
	packages=find_packages(),
	install_requires=['pyTelegramBotAPI', 'requests'],
)
