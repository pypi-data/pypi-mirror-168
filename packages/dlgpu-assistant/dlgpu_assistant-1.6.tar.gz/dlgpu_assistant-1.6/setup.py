from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="dlgpu_assistant",
    long_description=long_description,
    long_description_content_type='text/markdown',
    description = ("Use this tools to improve your ANN"),
    version="1.6",
    license="MIT",
    author="Rubén Hinojar",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "tensorflow-gpu==2.9.0",
        "pandas==1.4.3",
        "numpy==1.23.1",
        "scikit-learn==1.1.2"
    ],
)
