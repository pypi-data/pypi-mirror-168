from gettext import install
from struct import pack
from setuptools import setup, find_packages

setup(
    name="Mensajes-dcampinoa",
    version="6.0",
    description="Un paquete para saludar y despedir",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Daniela Campiño",
    author_email="dani.campino893@gmail.com",
    url="https://www.dani.dev",
    license_files=['LICENSE'],
    packages=find_packages(),
    scripts=[],
    test_suite='tests',
    install_requires=[paquete.strip() for paquete in open("requirements.txt").readlines()],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities'
    ]
)

# Para la distribución pública se aplican otros paquetes
## Cómo automatizar los paquetes


