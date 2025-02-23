from setuptools import setup, find_packages

setup(
    name="biteme-backend",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pymongo",
        "python-dotenv",
        "pytest",
        "httpx"
    ],
)