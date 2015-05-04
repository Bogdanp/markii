from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="markii",
    version="0.2.6",
    description="MarkII is a development-mode error handler for Python web applications.",
    long_description=long_description,
    packages=["markii", "markii.frameworks"],
    install_requires=["jinja2"],
    include_package_data=True,
    author="Bogdan Popa",
    author_email="popa.bogdanp@gmail.com",
    url="https://github.com/Bogdanp/markii",
    keywords=["web", "errors", "debugging"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ]
)
