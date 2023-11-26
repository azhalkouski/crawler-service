# crawler-service

# installing dependencies
  1. create a virtual env on your local machine: python3 -m venv env
  2. activate the virtual environment: source env/bin/activate
  3. install the dependencies: python3 -m pip install -r requirements.txt

# update requirements.txt command
  - pip freeze > requirements.txt

# fixing errors and enforcing the PEP 8 code standard
  **flake8**: Flake8 is a versatile tool that combines multiple linters,
  including PyFlakes, pycodestyle (formerly know as pep8), and McCabe
  complexity checker. It's a great choice for catching errors and
  enforcing PEP 8 style conventions.

  **black:** Black is an opinionated code formatter that automatically
  reformats code to comply with its style guide. WHile it doesnt'
  enforce PEP 8 exactly, it often produces code that aligns with
  PEP 8 standards.

  **isort:** FOr sorting and organizing imports according to PEP 8 guidelines,
  isort is a handy tool.

  Here's a common workflow using these tools:
    - Run **`flake8`** to catch errors and enforce PEP 8 style conventions.
    - Run **`black`** to automatically format code in a consistent style.
    - Run **`isort`** to organize sort imports.