from setuptools import setup, find_packages

setup(
    name="mastobot",
    version="0.2.1",
    description="Create cheap Mastodon bots in a Flask-like syntax",
    long_description=open("./README.md").read(),
    long_description_content_type="text/markdown",
    keywords="mastodon bot",
    license="0BSD",
    url="https://git.sr.ht/~fkfd/mastobot",
    author="Frederick Yin",
    author_email="fkfd@macaw.me",
    classifiers=["Development Status :: 3 - Alpha", "License :: Public Domain",],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=["Mastodon.py", "websockets", "lxml"],
)
