from setuptools import setup

setup(
    name="gpt-fhir",
    version="0.1",
    description="GPT-FHIR",
    author="Dzmitry Ashkinadze",
    author_email="dzmitry.ashkinadze@gmail.com",
    packages=["gpt_fhir"],
    install_requires=[
        "fhirclient",
        "ols_client",
        "langchain",
    ],
)
