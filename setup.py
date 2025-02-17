from setuptools import setup, find_packages

setup(
    name="biteme",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "openai",
        "requests",
        "pydantic",
        "python-dotenv",
        "uvicorn"
    ]
)