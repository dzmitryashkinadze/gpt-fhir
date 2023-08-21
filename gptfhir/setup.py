from setuptools import setup

setup(
    name='gptfhir',
    version='0.1.0',    
    description='A example Python package',
    author='Dima',
    author_email='test@test.gmail',
    packages=['gptfhir'],
    install_requires=[
        'langchain',
        'openai'                     
    ]
)