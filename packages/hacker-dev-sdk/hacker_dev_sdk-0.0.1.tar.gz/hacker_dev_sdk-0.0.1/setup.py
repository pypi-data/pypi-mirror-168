import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="hacker_dev_sdk",
  version="0.0.1",
  author="9eek",
  author_email="voodoos_hearty.0e@icloud.com",
  description="A useful, general SDK for hackers",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/shellfeel/HackerDevSdk.git",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3.8",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)