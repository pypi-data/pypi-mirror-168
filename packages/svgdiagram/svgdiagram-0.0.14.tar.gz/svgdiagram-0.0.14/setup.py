import setuptools
import subprocess
import os
import re
import json

_VERSION_FILE_PATH = os.path.join("svgdiagram/VERSION")
_REQUIREMENTS_FILE_PATH = os.path.join("svgdiagram/REQUIREMENTS")

if not os.path.isfile(_VERSION_FILE_PATH):
    # VERSION file does not exist, so it needs to be created
    # This assumes that the current git has has a tag
    svgdiagram_version = (
        subprocess.run(['git', 'describe', '--tags'], stdout=subprocess.PIPE)
        .stdout
        .decode('utf-8')
        .strip()
    )

    print(f"svgdiagram version: {svgdiagram_version}")

    assert re.fullmatch(r"\d+\.\d+\.\d+", svgdiagram_version), \
        f"No valid version found: {svgdiagram_version}!"

    with open(_VERSION_FILE_PATH, "w") as f:
        f.write(svgdiagram_version)
else:
    # VERSION file exists, meaning we are in the github deploy action
    # just read the file
    with open(_VERSION_FILE_PATH, "r") as f:
        svgdiagram_version = f.read().strip()

if not os.path.isfile(_REQUIREMENTS_FILE_PATH):
    # REQUIREMENTS file does not exist, so it needs to be stored
    # in the module to retain it for the second dist step
    with open("requirements.txt", "r") as f:
        requires = f.read().split()

    with open(_REQUIREMENTS_FILE_PATH, 'w') as f:
        json.dump(requires, f)
else:
    # REQUIREMENTS does exist, meaning we are in the github deploy action
    # just read the file
    with open(_REQUIREMENTS_FILE_PATH, "r") as f:
        requires = json.load(f)

setuptools.setup(
    name="svgdiagram",
    version=svgdiagram_version,
    author="Matthias Rieck",
    author_email="Matthias.Rieck@tum.de",
    description="Create SVG diagrams with python",
    long_description="Create SVG diagrams with python",
    url="https://github.com/MatthiasRieck/svgdiagram",
    packages=setuptools.find_packages(exclude=["tests*"]),
    package_data={"svgdiagram": ["VERSION", "REQUIREMENTS"]},
    include_package_data=True,
    requires=requires,
)
