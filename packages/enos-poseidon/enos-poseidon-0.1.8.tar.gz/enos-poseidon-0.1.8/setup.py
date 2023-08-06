import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

setup(
    name='enos-poseidon',
    version='0.1.8',
    description='ENOS API',
    long_description=README,
    author='Xiangxin Li',
    long_description_content_type='text/markdown',
    author_email='956217275@qq.com',
    url='https://github.com/EnvisionIot',
    license='GPLv3',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(),
    platforms=['all'],
    zip_safe=False,
    install_requires=[
        'pycryptodome>=3.8.2',
        'simplejson>=3.16.0',
    ],
)
