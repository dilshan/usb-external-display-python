import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="external_counter-dilshan",
    version="1.0.3",
    author="Dilshan R Jayakody",
    author_email="jayakody2000lk@gmail.com",
    description="Python API for USB seven segment display module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dilshan/usb-external-display-python",
    packages=setuptools.find_packages(),
    install_requires=[
        'pyserial',
    ],
    scripts=[
        'bin/usb-display-module-config',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
	"Operating System :: Microsoft :: Windows",
	"Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
	"Topic :: System :: Hardware",
	"Intended Audience :: Developers",
	"Natural Language :: English"
    ],
)
