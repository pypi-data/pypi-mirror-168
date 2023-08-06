from setuptools import setup, find_packages
  
with open("GameWidgets/README.md", "r") as fh:
    description = fh.read()
  
setup(
    name="GameWidgets",
    version="0.1.1",
    author="Manomay tyagi",
    author_email="tyagimanomay57@gmail.com",
    description="Pygame becomes easier",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/SuperGuy123456/GameWidgets",
    license='MIT',
    python_requires='>=3.8',
    install_requires=['pygame'],
    packages=find_packages()
)