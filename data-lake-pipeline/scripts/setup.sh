#!/bin/bash

# This script sets up the environment for the data-lake-pipeline project.
# It installs all necessary dependencies and sets up required configurations.

echo "Starting setup process..."

# Step 1: Update system packages
echo "Updating system packages..."
sudo apt-get update -y

# Step 2: Install Python 3 and pip (if not already installed)
echo "Installing Python 3 and pip..."
sudo apt-get install -y python3 python3-pip python3-venv

# Step 3: Install dependencies from requirements.txt
echo "Installing Python dependencies from requirements.txt..."
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt file not found!"
    exit 1
fi

# Step 4: Install Spark (if Spark is not already installed)
# Optional: You can comment this section if Spark is already installed in your environment
echo "Installing Apache Spark..."
if ! command -v spark-submit &> /dev/null; then
    echo "Spark not found. Installing Spark..."
    wget -qO- https://dlcdn.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.2.tgz | tar xvz -C /opt/
    sudo ln -s /opt/spark-3.3.2-bin-hadoop3.2 /opt/spark
    sudo echo "export PATH=$PATH:/opt/spark/bin" >> ~/.bashrc
    source ~/.bashrc
else
    echo "Spark is already installed."
fi

# Step 5: Set environment variables (if needed)
# You can add any environment variables here that are needed for your project (e.g., API keys)
echo "Setting up environment variables..."
export SPARK_HOME=/opt/spark
export PYSPARK_PYTHON=python3
export PYSPARK_DRIVER_PYTHON=python3

# Step 6: Verify the installation
echo "Verifying Python and Spark installations..."
python --version
pip show pyspark
spark-submit --version

echo "Setup process completed successfully!"
