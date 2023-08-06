from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='django-google-sheets',
    version='0.0.1',
    license='MIT License',
    author='issei momonge',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='mggyggf@gmail.com',
    keywords='django google sheets',
    description=u'Não é oficial do google',
    packages=['googlesheets'],
    install_requires=['gspread','django'],)