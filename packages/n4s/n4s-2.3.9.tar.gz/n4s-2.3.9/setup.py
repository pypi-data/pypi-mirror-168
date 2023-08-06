import setuptools, platform
from pip._internal import main as pip

with open('README.md') as f:
    long_description = f.read()

if platform.system() == "Darwin":
    pip(['install', '--user', 'appscript==1.2.0'])

pip(['install', '--user', 'beautifulsoup4==4.11.1'])
pip(['install', '--user', 'requests==2.27.1'])

setuptools.setup(
    name='n4s',
    version='2.3.9',
    author='Mike Afshari',
    author_email='theneed4swede@gmail.com',
    description='Collection of useful methods by Need4Swede',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/n4s/n4s',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)