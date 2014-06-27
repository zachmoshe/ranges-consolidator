from distutils.core import setup
import ranges_merger

setup(
		name='ranges-merger',
		version=ranges_merger.__version__,
		author='Zach Moshe',
		author_email='zachmoshe@gmail.com',
		packages=['ranges_merger'],
		scripts=[],
		url='https://github.com/zachmoshe/ranges-merger',
		license='LICENSE.txt',
		description='A package for merging together multiple (poetentially hierarchical) range sequences',
		long_description=open('README.md').read(),
		install_requires=[
			],
		)




