from setuptools import setup, find_packages

setup(
    name='yjdev_monitor',
    packages=find_packages(),
    install_requires=["sqlalchemy", "python-telegram-bot", "elasticsearch"]
)