from setuptools import setup, find_packages

setup(
    name='open-singly',
    version='0.1',
    description='Implementation of singly API for Python',
    author='Venelin Stoykov',
    author_email='venelin@magicsolutions.bg',
    url='https://github.com/MagicSolutions/open-singly',
    packages=find_packages(),
    zip_safe=False,
    install_requires=['slumber>=0.5.3'],
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
    ]
)
