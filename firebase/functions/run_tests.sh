#!/bin/bash
python -m unittest domain/tests/target_temprerature_test.py
python -m unittest models/tests/price_test.py
python -m unittest repositories/tests/heating_settings_test.py 
python -m unittest repositories/tests/prices_test.py 
