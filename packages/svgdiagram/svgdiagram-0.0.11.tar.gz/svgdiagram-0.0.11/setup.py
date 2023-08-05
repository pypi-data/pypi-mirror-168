import setuptools
import subprocess

svgdiagram_version = subprocess.run(
    ['git', 'describe', '--tags'],
    stdout=subprocess.PIPE,
).stdout.decode('utf-8').strip()

setuptools.setup(
    name="svgdiagram",
    version="0.0.11",
    author="Matthias Rieck",
    author_email="Matthias.Rieck@tum.de",
    description="Create SVG diagrams with python",
    long_description="Create SVG diagrams with python",
    url="https://github.com/MatthiasRieck/svgdiagram",
    packages=setuptools.find_packages(exclude=["tests*"]),
    requires=["yattag"]
)
