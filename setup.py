from setuptools import setup, find_packages

setup(
    name="SimpleBackUp",
    version="0.1.3",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "simplebackup=SimpleBackUp.__main__:main",
            "SimpleBackUp=SimpleBackUp.__main__:main",
        ],
    },
    author="TheCrafter",
    description="Ein kleiner Backup-Daemon mit JSON-Konfig",
    python_requires=">=3.8",
)
