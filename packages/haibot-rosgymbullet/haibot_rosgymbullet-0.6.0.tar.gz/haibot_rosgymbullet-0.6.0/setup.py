import setuptools
from pathlib import Path

setuptools.setup(
    name='haibot_rosgymbullet',
    version='0.6.0',
    description="DiffBot Ros-Gym-Bullet Environment",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="haibot_rosgymbullet*"),
    install_requires=['gym', 'pybullet', 'numpy', 'matplotlib']
)