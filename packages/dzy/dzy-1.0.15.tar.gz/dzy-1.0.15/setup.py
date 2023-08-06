"""
Setup dzy package
"""
from setuptools import setup, find_packages


setup(
    name="dzy",
    version="1.0.15",
    description="dzy Python package",
    author="dzy",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "freezegun>=1.1.0",
        "gcsfs>=2021.8.1",
        "google-cloud-bigquery>=2.23.2",
        "google-cloud-secret-manager>=2.7.2",
        "google-cloud-storage>=1.41.1",
        "pandas>=1.3.2",
        "pyarrow>=5.0.0",
        "pytz>=2021.1",
        "pyyaml>=6.0"
    ]
)
