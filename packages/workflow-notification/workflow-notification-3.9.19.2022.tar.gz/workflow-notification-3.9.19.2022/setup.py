import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="workflow-notification",
    version="3.09.19.2022",
    author="Nii Golightly",
    author_email="nlli@pm.me",
    description="workflow-notification ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nllii/workflow-notification.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)
