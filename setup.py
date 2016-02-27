from setuptools import setup

setup(
    name="markii",
    version="0.4.2",
    description="MarkII is a development-mode error handler for Python web applications.",
    long_description="https://github.com/Bogdanp/markii",
    packages=["markii", "markii.frameworks"],
    install_requires=["jinja2", "six"],
    include_package_data=True,
    author="Bogdan Popa",
    author_email="popa.bogdanp@gmail.com",
    url="https://github.com/Bogdanp/markii",
    keywords=["web", "errors", "debugging"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Debuggers"
    ]
)
