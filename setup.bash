export PYTHONPATH="$PWD"
source wsb-stonks/bin/activate
export FLASK_APP=main.py
export FLASK_ENV=development
export MONGO_URL=mongodb://localhost:27017/