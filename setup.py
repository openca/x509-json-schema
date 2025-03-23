from setuptools import setup, find_packages

setup(
    name='x509-json-schema',
    version='0.1.0',
    description='Validate digital certificates against a JSON schema.',
    author='Your Name',
    packages=find_packages(),
    package_data={'x509_json_schema': ['x509-schema.json']},
    entry_points={
        'console_scripts': [
            'cert-check=x509_json_schema.cert_check:main',
        ],
    },
    install_requires=[
        'cryptography',
        'jsonschema',
    ],
)