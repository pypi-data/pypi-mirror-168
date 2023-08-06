from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='lequanggminhhofficial',
    version='0.0.1',
    author='Lê Quang Minh',
    author_email='quangminh591@gmail.com',
    license='MIT',
    include_package_data = True,
    package_data={
    'mun_official.demo': ['mun_official/images/image1.png'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: pygame',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.2',
    ],
    keywords='pygame animation mun_official',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['pygame']
)