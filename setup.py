from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Temporal analysis of products statistical analysis package'
LONG_DESCRIPTION = 'A collection of methods for analyzing Temporal Analysis of Products (TAP) reactor data.'

# Setting up
# to create documentation (in docs) -> sphinx-aipdoc -o . .. -> make clean -> make html
setup(
        name="tapsap", 
        version=VERSION,
        author="M. Ross Kunz",
        author_email="<ross.kunz@inl.gov>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['numpy', 'pygam', 'csaps', 'cvxpy', 'pandas', 'nptdms', 'scipy', 'openpyxl', 'plotly', 'kaleido', 'multiprocess'], 
        
        keywords=['TAP', 'Temporal Analysis of Products', 'tapsap'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Science",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ],
        include_package_data=True,
        package_data={'': ['data/*.csv', 'data/*.tdms', 'data/*.xlsx']}
)