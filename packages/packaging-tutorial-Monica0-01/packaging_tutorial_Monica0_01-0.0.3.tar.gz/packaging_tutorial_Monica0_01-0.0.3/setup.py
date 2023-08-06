from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='packaging_tutorial_Monica0_01',
    version='0.0.3',
    packages=setuptools.find_packages(),
    url='https://github.com/pypa/sampleproject',
    license='MIT',
    author='zhangzimei',
    author_email='author@example.com',
    description='utils for myself',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['numpy', 'rdkit', 'pandas', 'matplotlib' ,'POT' ,'networkx' ,'py3Dmol' ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)