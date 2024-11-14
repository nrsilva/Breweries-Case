from setuptools import setup, find_packages

# Read the content of the README.md file for the long description of the package
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Setup configuration for the package
setup(
    name="data-lake-pipeline",  # Name of the package
    version="0.1.0",  # Version of the package
    author="Your Name",  # Author name
    author_email="youremail@domain.com",  # Author's email address
    description="Data pipeline for processing brewery data from the Open Brewery DB API",  # Short description of the package
    long_description=long_description,  # Long description (usually from the README.md)
    long_description_content_type="text/markdown",  # Type of content for the long description (Markdown)
    url="https://github.com/yourusername/data-lake-pipeline",  # URL to the project's GitHub (or another repository)
    packages=find_packages(where="src"),  # Locate the packages under the 'src' directory
    package_dir={"": "src"},  # Specifies the directory where the Python packages are located
    install_requires=[  # List of dependencies that will be installed automatically
        "apache-airflow==2.7.1",  # Apache Airflow for orchestrating the workflow
        "apache-airflow-providers-http==2.7.0",  # Airflow provider for HTTP integration (used for API calls)
        "pyspark==3.4.0",  # PySpark for distributed data processing
        "pandas==1.5.3",  # Pandas for data manipulation (optional, depending on your use case)
        "pyarrow==11.0.0",  # PyArrow for handling Parquet files (required for Spark)
        "requests==2.28.2",  # Requests for making HTTP requests (used to fetch data from the Open Brewery DB API)
        "pytest==7.2.2",  # Pytest for running tests
        "pytest-mock==3.10.0",  # Pytest mock for mocking during tests
        "pyyaml==6.0",  # PyYAML for reading configuration files (e.g., config.yaml)
        "numpy==1.23.5",  # NumPy for numerical operations (used by PySpark and Pandas)
        "docker==6.0.0",  # Docker Python library (if you are interacting with Docker programmatically)
        "loguru==0.6.0"  # Loguru for enhanced logging support
    ],
    classifiers=[  # Additional metadata for the package, useful for repositories like PyPI
        "Programming Language :: Python :: 3",  # Specifies that this package is for Python 3
        "License :: OSI Approved :: MIT License",  # License type for the project
        "Operating System :: OS Independent",  # The package is OS independent
    ],
    python_requires='>=3.8',  # Minimum Python version required for the package
    entry_points={  # Optional: Define console scripts (commands that can be run from the terminal)
        'console_scripts': [
            'run-pipeline=scripts.run_pipeline:main',  # Example entry point for running the pipeline script
        ],
    },
    include_package_data=True,  # Includes additional package data like configuration files
)

