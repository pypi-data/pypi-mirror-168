from setuptools import setup

setup(
    name="dicom_cnn",
    version="0.0.1",
    url="https://github.com/Pixilib/dicom_cnn",
    python_requires="~=3.9",
    description="Librairie to sort - process dicom to feed CNN models",
    packages=["dicom_cnn"],
    package_dir={"": "src"},
)