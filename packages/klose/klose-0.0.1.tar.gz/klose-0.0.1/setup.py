import setuptools

with open("readme.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="klose",
    version="0.0.1",
    author="miro",
    author_email="619434176@qq.com",
    description="pity internal package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wuranxu/klose",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
