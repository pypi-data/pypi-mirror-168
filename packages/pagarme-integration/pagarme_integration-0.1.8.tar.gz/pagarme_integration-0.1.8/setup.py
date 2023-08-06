from setuptools import setup, find_packages

setup(
    name="pagarme_integration",
    version="0.1.8",
    description="Pagarme API",
    author="Caiqui Fhelipe and Juan Pablo",
    author_email="developer.cfms@gmail.com",
    url="https://github.com/caiquilipe/pagarme_integration",
    download_url="https://github.com/caiquilipe/pagarme_integration",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests", "jsonschema"],
    zip_safe=False,
)
