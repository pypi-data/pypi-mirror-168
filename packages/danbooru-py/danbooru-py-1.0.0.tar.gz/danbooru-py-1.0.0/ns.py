import setuptools
from danbooru import __version__
#python ns.py sdist bdist_wheel
#python -m twine upload dist/*

setuptools.setup(
    name="danbooru-py",
    version=__version__,
    license="MIT",
    author="VoidAsMad",
    author_email="voidasmad@gmail.com",
    description="단보루 크롤링 라이브러리",
    long_description=open("README.md", "rt", encoding="UTF8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Tanukixi/Danbooru/tree/main/SDK",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)