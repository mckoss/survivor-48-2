from setuptools import setup, find_packages

setup(
    name="survivor-48-2",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # Add your project dependencies here
    ],
    entry_points={
        'console_scripts': [
            'survivor-48-2=main:main',
        ],
    },
)
