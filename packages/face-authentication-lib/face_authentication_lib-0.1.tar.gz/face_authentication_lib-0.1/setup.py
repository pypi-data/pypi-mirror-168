from codecs import open
from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='face_authentication_lib',
    version='0.1',
    description='Setting up a python face authentication package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    author='SamanAI',
    author_email='info@saman.ai',
    license='MIT',
    packages=find_packages(),
    keywords=['AI', 'face authentication', 'face detection'],
    install_requires=[
        'requests==2.20.0'
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    include_package_data=True,
)
