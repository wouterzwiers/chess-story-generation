import setuptools

with open("README.md", 'r') as file:
    long_description = file.read()

setuptools.setup(
    name="chess-story-generation",
    version='0.0.1',
    author="Timon Steuer",
    author_email="t.steuer@live.com",
    description="Chess-Story-Generation",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/TimonSteuer/chess-story-generation.git",
    packages=setuptools.find_packages(),
    install_requires=[
        "chess",
        "python-chess",
        "PyYAML"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
