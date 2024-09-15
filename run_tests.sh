#!/bin/bash

# Activate virtual environment (replace with your activation command)
venv\Scripts\Activate  # Example using virtualenv

# Run the tests using pytest
pytest test.py

# Check the exit code of pytest
if [[ $? -eq 0 ]]; then
  echo "Tests Passed!"
  # Exit with success code (0)
else
  echo "Tests Failed!"
    # Exit with failure code (1)
fi
sleep 3
