from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='teachable_machine',
    version='1.0',
    description='A Python package to simplify the deployment process of exported Teachable Machine models.',
    py_modules=["teachable_machine"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",

    install_requires=[
        "numpy",
        "Pillow",
        "tensorflow",
    ],
    # extra_require={
    #     "dev": [
    #         "pytest>=3.7",
    #     ]
    # },

    url="https://github.com/MeqdadDev/teachable-machine",
    author="Meqdad Dev",
    author_email="meqdad.darweesh@gmail.com",

)
