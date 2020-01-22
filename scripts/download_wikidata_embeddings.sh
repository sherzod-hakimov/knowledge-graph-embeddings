### Pretrained Wikidata embeddings https://torchbiggraph.readthedocs.io/en/latest/pretrained_embeddings.html
### 200 dimensions

SOURCEDIR="wikidata_dim_200"

if [ ! -d "$SOURCEDIR" ]; then
  mkdir -p $SOURCEDIR
fi

cd $SOURCEDIR

echo "Downloading the Wikidata embeddings"
wget https://dl.fbaipublicfiles.com/torchbiggraph/wikidata_translation_v1.tsv.gz

cd ..