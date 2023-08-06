from os.path import exists
from setuptools import setup, find_packages

setup(
    name='bs-pathutils',
    version='0.1.0',
    author="Bill Schumacher",
    author_email="34168009+BillSchumacher@users.noreply.github.com",
    packages=find_packages(),
    url="https://github.com/BillSchumacher/bs-pathutils",
    license="MIT",
    description="Extracts Django's built-in templates and statics.",
    long_description=open("README.md").read() if exists("README.md") else "",
    long_description_content_type='text/markdown',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
    ],
)
