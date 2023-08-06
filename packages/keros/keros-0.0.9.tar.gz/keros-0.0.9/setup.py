from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='keros',
    version='0.0.9',
    license='MIT License',
    author='Armando Luz Borges',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='armandoari.288@gmail.com',
    description=u'Pacote destinado ao uso de conceitos de machine learning',
    packages=['keros'],
    install_requires=['numpy', 'scikit-learn', 'scikit-image', 'rich'])