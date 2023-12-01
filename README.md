# crawler-service

# installing dependencies
  1. create a virtual env on your local machine: python3 -m venv env
  2. activate the virtual environment: source env/bin/activate
  3. install the dependencies: python3 -m pip install -r requirements.txt

# run the service in development mode
  From the root directory
  - Step 1: `python3 -m install -e .` - install in editable mode
  - Step 2.1: `python3 -m crawler_service`
  - Step 2.2: `python3 -m crawler_service selenium_headless` - selenium headless mode

# run test along with coverage
  - `coverage run -m pytest tests/ && coverage report -m && coverage html && coverage json --pretty-print`

# fixing errors and enforcing the PEP 8 code standard
  - ruff check .
  - ruff check --fix .
