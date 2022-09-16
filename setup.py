import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='openimis-be-self-registration',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    license='GNU AGPL v3',
    description='The openIMIS self registration reference module.',
    # long_description=README,
    url='https://openimis.org/',
    author='Tinker Technology',
    author_email='info@tinker.com.np',
    install_requires=[
        'django',
        'django-db-signals',
        'djangorestframework',
        'openimis-be-core',
        'openimis-be-claim_batch',
        'openimis-be-insuree',
        'openimis-be-location',
        'openimis-be-medical',
        'openimis-be-policy',
        'openimis-be-product',
        'openimis-be-report',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
