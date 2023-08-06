from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name = 'locust-jtl-logger',
    version = '0.0.1',
    author = 'Henning Seljenes',
    author_email = 'henning.seljenes@gmail.com',
    license = 'MIT',
    description = 'Locust listener class that logs to a jmeter JTL CSV',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/hseljenes/locust-jtl-logger',
    py_modules = ['locust_jtl_logger'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ]
)