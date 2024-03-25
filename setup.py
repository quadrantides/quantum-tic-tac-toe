from setuptools import setup
from setuptools import find_packages

setup(
    name='qt3',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "qt3=qt3.main"
        ]
    },
    url='https://github.com/quantum-tic-tac-toe',
    version="1.0",
    description='Quantum Tic Tac Toe game',
    zip_safe=False,
    license='Public',
    platforms='Linux',
    maintainer='quadrantides',
    maintainer_email='github@quadrantides.com')
