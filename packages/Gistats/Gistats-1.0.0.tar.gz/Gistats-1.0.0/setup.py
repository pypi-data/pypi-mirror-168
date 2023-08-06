from setuptools import setup

long_description = open('./README.md')

setup(
    name='Gistats',
    version='1.0.0',
    url='https://github.com/ZSendokame/Gistats',
    license='MIT license',
    author='ZSendokame',
    description=' Generate nice Statistics in your gists.',
    long_description=long_description.read(),
    long_description_content_type='text/markdown'
)