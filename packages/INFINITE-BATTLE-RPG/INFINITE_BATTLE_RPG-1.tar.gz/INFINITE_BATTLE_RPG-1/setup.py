from setuptools import setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description


setup(
    name='INFINITE_BATTLE_RPG',
    version='1',
    packages=['INFINITE_BATTLE_RPG'],
    url='https://github.com/PythonApkDev/PythonApkDev.github.io/tree/main/beginner-projects/INFINITE_BATTLE_RPG',
    license='MIT',
    author='PythonApkDev',
    author_email='pythonapkdev2022@gmail.com',
    description='This package contains implementation of the offline RPG '
                '"INFINITE_BATTLE_RPG" on command line interface.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
    entry_points={
        "console_scripts": [
            "INFINITE_BATTLE_RPG=INFINITE_BATTLE_RPG.infinite_battle_rpg:main",
        ]
    }
)