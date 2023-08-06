from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="UTF-8")

setup(
    name="jk_contract",
    version="1.0.8",
    description="Toolkit with functions designed to extract various information from JK contracts", 
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OvergrownBaby/jk_contract",
    author="Andy Tsang Yuk Lun",
    author_email="andytsangyuklun@gmail.com", 
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7, <4",
    install_requires=["docx2python", "regex", "pandas", "numpy"],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        "console_scripts": [
            "jk_contract=jk_contract:main",
        ],
    },
    project_urls={  # Optional
        "PyPi": "https://pypi.org/project/jk-contract/",
    },
)