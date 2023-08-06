from setuptools import setup, find_packages
with open("README.md", "r") as readme_file:
    readme = readme_file.read()

#requirements = ["wheel==0.37.1","twine==1.13.0"]

setup(
    name="testprojectrajlaxmi",
    version="0.0.1",
    author="Rajlaxmi Dharmpuriwar",
    description="A package to say hello world",
    long_description=readme,
    long_description_content_type="text/markdown",
    #url="https://github.com/your_package/homepage/",
    packages=find_packages(),
    install_requires=["numpy"],
    classifiers=[
        "Programming Language :: Python :: 3.10"
    ],
)