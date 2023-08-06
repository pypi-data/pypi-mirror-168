from setuptools import setup

setup(
    name = 'TCGCSUtils',
    version = '1.0.7',
    author = 'Maycon Vinicius Guimarães',
    author_email = 'maycon.guimaraes@tc.com.br',
    packages = ['TCGCSUtils'],
    install_requires = [
        "gcsfs==2022.8.2",
        "ndjson==0.3.1",
        "numpy==1.23.3",
        "pandas==1.4.4",
        "pyarrow==7.0.0",
        "python-dateutil==2.8.2",
        "google-cloud-storage==2.5.0",
    ],
    description='A lib to easily save or read files in GCS',
)
