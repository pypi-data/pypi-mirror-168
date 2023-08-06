from setuptools import find_packages, setup

setup(
    name="Paperl",
    version="0.0.1.alpha10",
    author="XiangQinxi",
    author_email="XiangQinxi@outlook.com",
    description="使用tkinter开发高级GUI调试库",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    install_requires=[
        "colorama"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests"]),
    package_data={"": ["*.gif"]},
    include_package_data=True,
)
