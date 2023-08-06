from setuptools import setup
from pathlib import Path

# Program metadata

PROGRAM_ID = "gentexdoc"
PROGRAM_VERSION = "0.4.1"


directory = Path(__file__).parent

setup(
    name=PROGRAM_ID,
    version=PROGRAM_VERSION,
    packages=[PROGRAM_ID],
    entry_points={
        "console_scripts": [f"{PROGRAM_ID}={PROGRAM_ID}.main:main"],
    },
    author='Pursuit',
    author_email='fr.pursuit@gmail.com',
    description='Markdown to Latex to PDF generator',
    long_description=(directory / "README.md").read_text(encoding="utf-8"),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/frPursuit/gentexdoc',
    license='GNU General Public License v3 (GPLv3)',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=['Jinja2>=3.1.2']
)
