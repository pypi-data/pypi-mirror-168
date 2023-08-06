from distutils import extension
import setuptools
from Cython.Build import cythonize
from dotenv import Dotenv
import os

cython_args = {}

if os.getenv("SURREAL_BUILD_NO_COMPLIE") != "1" or Dotenv("./.env").get("SURREAL_BUILD_NO_COMPLIE") != "1":
    cython_args = {"ext_modules": cythonize("surreal/surreal_compiled.py", language_level=3)}

setuptools.setup(
    name="surreal-db-python",
    version="0.0.1",
    description="Python client for the Surreal Database (Websocket not supported)",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author="Rukchad Wongprayoon",
    author_email="contact@rukchadisa.live",
    url="https://github.com/timelessnesses/surreal-db-python",
    packages=['surreal'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Database",
        "Typing :: Typed"
    ],
    install_requires="requests aiohttp yarl".split(" "),
    extras_require={
        "orjson": ["orjson"]
    },
    **cython_args
)
