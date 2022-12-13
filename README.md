# GEO-Query
you may need to request access from https://cors-anywhere.herokuapp.com/corsdemo for live demo purpose.  
For live demo, please access https://aileenlin.github.io/geo-query/, 

## Environment preparation
```bash
pip install pyserini, flask, flask_restful, flask_cors
```

## Data preparation
```bash
cd data_prepare
# these steps require ~40GB memory and > 2TB free disk space.
# wikidata query server will be start on port 7001
bash wikidata.sh
# mmead query server will be start on port 7015
bash mmead.sh
# pyserini passage retrieval server will be start on port 9527
python anserni_server.py --server_host 0.0.0.0 --server_port 9527
```

## Front end setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```
