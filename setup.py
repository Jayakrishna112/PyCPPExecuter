from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='PyCPPExecuter',
    version='1.0.0',
    description="This is a module that uses python interface to execute the c/c++ programs and perform actions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Jayakrishna112/PyCPPExecuter',
    author="JayaKrishna",
    author_email="jayakrishnamarni1234@gmail.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'gcc-install = PyCPPExecuter:compiler_installer',
        ],
    },
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0"],
    },
    python_requires=">=3.10"
)
