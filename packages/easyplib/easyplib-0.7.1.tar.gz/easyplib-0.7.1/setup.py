from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='easyplib',
    version='0.7.1',
    author="Alexander Timofeev",
    author_email="tam2511@mail.ru",
    python_requires=">=3.6",
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tam2511/EasyPL",
    install_requires=[
        'pytorch-lightning >= 1.7.0',
        'torch >= 1.12.0',
        'pandas',
        'dill',
        'opencv-python',
        'matplotlib',
        'albumentations',
        'torchvision >= 0.13.0',
        'torchmetrics >= 0.9.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)