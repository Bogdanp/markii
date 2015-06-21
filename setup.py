from setuptools import setup

setup(
    name="markii",
    version="0.3.2",
    description="MarkII is a development-mode error handler for Python web applications.",
    long_description="https://github.com/Bogdanp/markii",
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
