# KB-Embedding


Steps for training knowledge graph embeddings for DBpedia:

1) Run the `bash scripts/install_open_ke.sh` script -> clones the git repo for OpenKE and builds it
2) Run the `bash scripts/download_dbpedia_triples.sh` script -> downloads needed triples from DBpedia server and preprocesses them
3) Install python dependencies given in "requirements.txt", e.g. `pip install -r requirements.txt`
4) Run the `bash scripts/generate_training_files.sh` script -> generates the needed file formats for OpenKE
5) Run the training script `bash scripts/train.sh` -> you can edit the "config.json" for changing dimensions, epochs, optimizers, etc., e.g. https://github.com/thunlp/OpenKE/tree/OpenKE-PyTorch#step-2-set-configure-parameters-for-training


Steps for training knowledge graph embeddings for Wikidata:

1) Run the `bash scripts/install_open_ke.sh` script -> clones the git repo for OpenKE and builds it
2) Run the `bash scripts/download_wikidata_triples.sh` script -> downloads needed triples from DBpedia server and preprocesses them
3) Install python dependencies given in "requirements.txt", e.g. `pip install -r requirements.txt`
4) Run the python script `python extract_wikidata_triples.py -i latest-all.nt.gz`
4) Run the `bash scripts/generate_training_files.sh` script -> generates the needed file formats for OpenKE
5) Run the training script `bash scripts/train.sh` -> you can edit the "config.json" for changing dimensions, epochs, optimizers, etc., e.g. https://github.com/thunlp/OpenKE/tree/OpenKE-PyTorch#step-2-set-configure-parameters-for-training


Download pretrained Wikidata Embeddings
1) Run the `bash scripts/download_wikidata_embeddings.sh` script -> downloads pretrained 200-dimensional download_wikidata_embeddings into the folder "wikidata_dim_200"
2) Run `python extract_wikidata_embeddings.py` -> extracts embeddings for Wikidata entity and relations. Embeddings will be saved under "wikidata_dim_200/entity_embeddings.txt" and "wikidata_dim_200/relation_embeddings.txt" .
The embedding files are formatted as follows: The first line indicates the number of URIs and the dimension size. The next lines are URIs and embedding vector. The lines are separated by space.
