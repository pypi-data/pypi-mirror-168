from setuptools import find_packages, setup

from slackminion.plugins.core import version

setup(
    name="slackminion",
    version=version,
    packages=find_packages(exclude=["test_plugins"]),
    url="https://github.com/pinterest/slackminion",
    license="MIT",
    author="Pinterest, Inc.",
    author_email="",
    description="A python bot framework for slack",
    package_data={"slackminion": ["templates/*"]},
    python_requires=">=3.7",
    install_requires=[
        "Flask>=1.1.1",
        "itsdangerous>=0.24",
        "Jinja2>=2.10",
        "MarkupSafe>=0.23",
        "PyYAML>=4.2b",
        "requests >=2.11, <3.0a0",
        "slack_sdk==3.18.3",
        "websocket-client >=0.35, <0.55.0",
        "Werkzeug>=0.10.4",
        "aiohttp>=3.7.4.post0",
    ],
    entry_points={
        "console_scripts": [
            "slackminion = slackminion.__main__:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Communications :: Chat",
    ],
)
