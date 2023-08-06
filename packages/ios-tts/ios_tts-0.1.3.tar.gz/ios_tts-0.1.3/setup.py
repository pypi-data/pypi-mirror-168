try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

with open('README.md', 'r') as f:
	long_description = f.read()

with open('ios_tts/version.py', 'r') as f:
	x = f.read()
	y = x[x.index("'")+1:]
	z = y[:y.index("'")]
	version = z

setup(
	name='ios_tts',
	packages=['ios_tts'],
	version=version,
	description='a unitts driver for ios device, it use AVFoundation.AVSpeechSynthesizer',
	author='Yu Moqing',
	url='https://github.com/yumoqing/ios_tts',
	long_description=long_description,
	long_description_content_type="text/markdown",
	author_email='yumoqing@gmail.com',
	# install_requires=install_requires ,
	keywords=['pyttsx' , 'ios', 'offline tts engine'],
	classifiers = [
		'Intended Audience :: End Users/Desktop',
		'Intended Audience :: Developers',
		'Intended Audience :: Information Technology',
		'Intended Audience :: System Administrators',
		'Operating System :: OS Independent',
		'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
		'Programming Language :: Python :: 3'
	],
)
