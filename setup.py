from setuptools import setup, find_packages


def get_long_description():
    with open('./README.rst', 'r') as readme:
        return readme.read()

setup(
    name='open-singly',
    version='0.2',
    description='Implementation of singly API for Python',
    author='Venelin Stoykov',
    author_email='venelin@magicsolutions.bg',
    url='https://github.com/MagicSolutions/open-singly',
    long_description=get_long_description(),
    packages=find_packages(),
    zip_safe=True,
    install_requires=['slumber>=0.5.3'],
    include_package_data=True,
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
    ]
)
