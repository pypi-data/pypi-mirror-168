from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='django-google-keys',
    version='0.0.2',
    license='MIT License',
    author='issei momonge',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='mggyggf@gmail.com',
    keywords='django key',
    description=u'Não é oficial do google',
    packages=['django_key'],
    install_requires=['yake','bs4'],)