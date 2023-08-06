import versioneer
from setuptools import setup, find_packages


with open('requirements.txt') as file:
    REQUIREMENTS = file.readlines()

with open('README.md') as file:
    README = file.read()


setup(
    name='drb-metadata',
    packages=find_packages(include=['drb_metadata']),
    description='DRB Metadata Extractor',
    long_description=README,
    long_description_content_type='text/markdown',
    author='GAEL Systems',
    author_email='drb-python@gael.fr',
    url='https://gitlab.com/drb-python/metadata/metadata',
    python_version='>=3.8',
    install_requires=REQUIREMENTS,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    package_data={'drb_metadata': ['schema.yml']},
    data_files=[('.', ['requirements.txt'])],
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass()
)
