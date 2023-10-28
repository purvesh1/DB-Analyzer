#!/bin/bash

# Create subdirectories for different components
mkdir -p src src/config src/utils src/tests

cd src

# Create Python files for different modules

touch __init__.py main.py database_interaction.py llm_integration.py nlp_processing.py data_analysis.py cli_interface.py

cd config

# Create a configuration file
touch config.py

cd utils

# Create utility files
touch __init__.py helpers.py db_utils.py

cd tests

# Create test files
touch __init__.py test_database_interaction.py test_llm_integration.py test_nlp_processing.py test_data_analysis.py

cd ..

# Create a README and requirements file
touch README.md requirements.txt
touch .gitignore
touch config/__init__.py src/__init__.py utils/__init__.py

echo 'Project structure created successfully.'