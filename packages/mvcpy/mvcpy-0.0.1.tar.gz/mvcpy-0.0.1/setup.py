import setuptools
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setuptools.setup(
	name = "mvcpy",
	version = "0.0.1",
	author = "Abdulsalam Raja",
	description = "molecularclustering",
	long_description = long_description,
	packages = ["mvcpy"],
	long_description_content_type='text/markdown'
)