#!/usr/bin/env python3
from pathlib import Path

from setuptools import find_packages, setup

ROOT = Path(__file__).parent
README = ROOT / "agent_harness/README.md"


def read_readme():
    try:
        return README.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


setup(
    name="gui-agent-harness",
    version="1.0.0",
    author="CLI Anything Contributors",
    description="GUI agent harness built on Vercel Labs agent-browser",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/HKUDS/CLI-Anything",
    project_urls={
        "Homepage": "https://github.com/HKUDS/CLI-Anything",
        "Issues": "https://github.com/HKUDS/CLI-Anything/issues",
    },
    license="MIT",
    packages=find_packages(include=["agent_harness*"]),
    python_requires=">=3.10",
    install_requires=[
        "click>=8.1,<9.0",
        "prompt-toolkit>=3.0,<4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7",
            "pytest-cov>=4",
            "build",
            "twine",
        ],
    },
    entry_points={
        "console_scripts": [
            "gui-agent-harness=agent_harness.gui_agent_harness_cli:main",
        ],
    },
    package_data={
        "agent_harness": [
            "skills/*.md",
            "skills/references/*.md",
            "skills/references/*/*.md",
            "skills/evals/*.md",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="gui harness browser automation agent-browser ai-agent evals",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
