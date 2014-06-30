from distutils.core import setup
import ranges_consolidator


setup(
		name='ranges-consolidator',
		packages=['ranges_consolidator'],
		version=ranges_consolidator.__version__,
		author='Zach Moshe',
		author_email='zachmoshe@gmail.com',
		scripts=[],
		url='https://github.com/zachmoshe/ranges-consolidator',
		download_url='https://github.com/zachmoshe/ranges-consolidator/tarball/1.0.0',
		license='LICENSE.txt',
		description='A package for flattening and consolidating multiple (potentially hierarchical) range sources (iterators over Range objects)',
		long_description="For documentation, visit the `GitHub page <https://github.com/zachmoshe/ranges-consolidator>`_",
		keywords=['range', 'flatten', 'hierarchy', 'consolidate', 'merge', 'whois', 'ip', 'allocation'],
    classifiers=[
	    "Development Status :: 5 - Production/Stable",
	    "Intended Audience :: Developers",
	    "License :: OSI Approved :: MIT License",
	    "Programming Language :: Python :: 2.7",
	    "Programming Language :: Python :: 3.4",
	    "Topic :: Utilities",
		],

)




