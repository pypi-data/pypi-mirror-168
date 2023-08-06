from setuptools import setup, find_packages

description = open('README.md', 'r', encoding='utf-8').read()

setup(name='strictTyping', version='0.1.4', packages=find_packages(), long_description=description, long_description_content_type='text/markdown')
