import pathlib
import pkg_resources
from setuptools import setup, find_packages

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]


setup(
    name='password manager',
    version='0.1',
    description='Simple Password Manager',
    url='https://github.com/jeswanthmukesh20/PasswordManager.git',
    author='Jeswanth Mukesh',
    author_email='github@jeswanthmukesh20.com',
    license='MIT',
    install_requires=install_requires,
    packages=find_packages(),
    entry_points=dict(
        console_scripts=['rq=src.main:display_quote']
    )
)
