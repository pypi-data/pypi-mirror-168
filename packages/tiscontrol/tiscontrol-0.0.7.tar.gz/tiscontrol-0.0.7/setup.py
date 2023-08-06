import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='tiscontrol',
    version='0.0.7',
    description='Python library to provide a reliable communication link with TIS  Products',
    url='https://github.com/GeoffAtHome/lightwave',
    author='tiscontrol',
    author_email='gopaltis93@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=setuptools.find_packages(),
    keywords=['tiscontrol'],
    zip_safe=False
)
