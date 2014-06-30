from distutils.core import setup
import ranges_consolidator

setup(
		name='ranges-consolidator',
		version=ranges_consolidator.__version__,
		author='Zach Moshe',
		author_email='zachmoshe@gmail.com',
		packages=['ranges_consolidator'],
		scripts=[],
		url='https://github.com/zachmoshe/ranges-consolidator',
		license='LICENSE.txt',
		description='A package for consolidating multiple (poetentially hierarchical) range sources (iterators over Range objects)',
		long_description=open('README.md').read(),
		install_requires=[
			],
		)




