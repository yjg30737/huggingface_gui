from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name='huggingface-gui',
    version='0.0.142',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    package_data={'huggingface_gui': ['hf-logo.svg']},
    description='Manage HuggingFace models with Python desktop app',
    url='https://github.com/yjg30737/huggingface-gui.git',
    long_description_content_type='text/markdown',
    long_description=long_description,
    install_requires=[
        'PyQt5>=5.14',
        'huggingface_hub',
        'transformers',
        'diffusers'
    ]
)