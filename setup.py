#!/usr/bin/env python
import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='pycryptotools',
    version='0.2.1',
    description='Python Crypto Coin Tools',
    long_description=open('README.md').read(),
    long_description_content_type= 'text/markdown',
    author='Toporin',
    author_email='satochip.wallet@gmail.com',
    url='https://github.com/Toporin/pycryptotools',
    project_urls={
        'Github': 'https://github.com/Toporin',
        'Webshop': 'https://satochip.io/',
        'Telegram': 'https://t.me/Satochip',
        'Twitter': 'https://twitter.com/satochipwallet',
        'Source': 'https://github.com/Toporin/pycryptotools',
        'Tracker': 'https://github.com/Toporin/pycryptotools/issues',
    },
    install_requires=requirements,
    packages=setuptools.find_packages(),
    package_dir={
        'pycryptotools': 'pycryptotools'
    },
    package_data={
        'pycryptotools': ['*.txt'],
    },
    scripts=['cryptotool'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Security :: Cryptography',
    ],
    python_requires='>=3.6',
)
