# WSB stonks

## To run locally:
Step 0:
- comment out line 2 in backend/app/tasks/nlp_engine/analysis.py (if you downloaded NLTK data to some central location on your machine)
- (Alternatively) make a nltk_data directory under "backend" and download stopwords and wordnet from NLTK into it (if you want to use bare minimum disk space and have the data locally)

In terminal 1:

```
$ cd backend
$ export MONGO_URL="mongodb+srv:/username:password@secret_MongoDB_Atlas_cluster_location_on_gcp"
$ export FLASK_APP=main.py
$ flask run
```

In terminal 2:

```
$ cd frontend
$ yarn start # or npm install && npm start
```

## NLP

Observations:

- Notice that stocks not always are in capital letters
- Text can contain links
- Typically stocks are NN
