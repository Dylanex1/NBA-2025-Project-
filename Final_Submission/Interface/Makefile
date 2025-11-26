# Variabes
PYTHON = python3
PIP = pip3

all:
	$(PIP) install pymssql pandas

run:
	$(PYTHON) main.py

# For Mac and Linux only
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -r {} +