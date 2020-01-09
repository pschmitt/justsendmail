from setuptools import find_packages, setup


setup(
    name="justsendmail",
    version="1.0",
    license="GPL3",
    description="Simple lib to send mail",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': ['justsendmail=justsendmail.mail:main'],
    },
    author="Philipp Schmitt",
    author_email="philipp@schmitt.co",
    url="https://github.com/pschmitt/pymail_utils",
    packages=find_packages(),
    include_package_data=True
)
