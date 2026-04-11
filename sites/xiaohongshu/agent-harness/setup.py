#!/usr/bin/env python3
from pathlib import Path

from setuptools import find_packages, setup

ROOT = Path(__file__).parent
README = ROOT / "cli_anyweb/xiaohongshu/README.md"


def read_readme():
    try:
        return README.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


setup(
    name="cli-anyweb-xiaohongshu",
    version="0.1.0",
    author="CLI Anything Contributors",
    description="Standalone cli-anyweb harness for xiaohongshu",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(include=["cli_anyweb", "cli_anyweb.*"]),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "cli-anyweb-xiaohongshu=cli_anyweb.xiaohongshu.xiaohongshu_cli:main",
        ],
    },
    package_data={
        "cli_anyweb.xiaohongshu": [
            "README.md",
            "skills/*.md",
            "skills/references/*.md",
            "skills/evals/*.yaml",
            "tests/*.md",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
