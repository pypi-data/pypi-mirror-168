from setuptools import setup, find_packages
import os

with open(os.path.join("/Users/ishi/microkinetic_toolkit", "README.md")) as f:
    long_description = f.read()

PACKAGES=[
	"microkinetic_toolkit",
	"microkinetic_toolkit.preparation",
	"microkinetic_toolkit.visualization",
	"microkinetic_toolkit.openfoam"
]

URL="https://github.com/atsushi-ishikawa/microkinetic_toolkit"

setup(
	name="microkinetic_toolkit",
	version="0.0.0",
	description="Python library for microkinetic analysis in catalytic chemistry.",
    url=URL,
    download_url=URL,
    long_description=long_description,
    long_description_content_type="text/markdown",
	author="Atsushi Ishikawa, Haruyuki Oda",
	author_email="ishikawa.atsushi@nims.go.jp",
	maintainer="Atsushi Ishikawa",
	maintainer_email="ishikawa.atsushi@nims.go.jp",
	license="MIT",
	packages=PACKAGES
)

