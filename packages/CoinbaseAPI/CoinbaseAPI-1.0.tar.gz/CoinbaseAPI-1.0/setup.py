import setuptools
with open(r'C:\Users\baccaraaa\Downloads\README (2).md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='CoinbaseAPI',
	version='1.0',
	author='billiedark',
	author_email='hhxx213@gmail.com',
	description='Easy Coinbase API for simple payment acceptance',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/billiedark/CoinbaseAPI',
	packages=['CoinbaseAPI'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)