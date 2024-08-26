#/bin/sh

# [Update to your project weather path!] specify the testing path for -m pytest 
if [ -z "$PYTHONPATH" ]; then
  export PYTHONPATH="/Users/kai/Documents/projects/flask-weather-api/weather:$PYTHONPATH"
fi

python -m pytest tests/conftest.py
python -m pytest tests/test_db.py
python -m pytest tests/test_factory.py
python -m pytest tests/test_weather.py