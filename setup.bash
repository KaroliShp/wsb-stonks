export PYTHONPATH="$PWD"
source wsb-stonks/bin/activate
export FLASK_APP=main.py
export FLASK_ENV=development
export MONGO_URL="mongodb+srv:/username:password@secret_MongoDB_Atlas_cluster_location_on_gcp"