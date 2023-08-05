import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot_plugin_bottle",
    version="0.1",
    author="Todysheep",
    author_email="todysheep@163.com",
    description="Bottle post plugin in Nonebot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Todysheep/nonebot_plugin_bottle",
    packages=setuptools.find_packages(),
    install_requires=[],
    entry_points={},
    license='GNU GPLv3',
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)