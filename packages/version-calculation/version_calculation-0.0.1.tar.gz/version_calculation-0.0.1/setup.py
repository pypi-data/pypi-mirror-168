from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='version_calculation',
    version='0.0.1',
    license='MIT License',
    author='issei momonge',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='mggyggf@gmail.com',
    keywords='calculadora de versão',
    description=u'uma calculadora de opreções basicas para versões',
    packages=['version_calculation'],
    install_requires=[''],)