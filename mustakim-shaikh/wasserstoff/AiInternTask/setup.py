from setuptools import setup, find_packages

setup(
    name='pdf_processor',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'PyPDF2',
        'pymongo'
    ],
)

