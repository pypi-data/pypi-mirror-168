from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Demonstrating how to use test.PyPI'



setup(
    # name des paketes auf dem Package index
    name="package_pku",
    version=VERSION,
    author="ExperTeach GmbH",
    author_email="et_pku@web.de",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas'
        ],
    keywords=[
        'python',
        'code',
        ' Expertttt'  
        ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
