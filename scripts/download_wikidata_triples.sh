#### Script for downloading DBpedia files and preprocess them
#### Adapted from https://github.com/dice-group/KG-NMT/blob/master/KGE_creation.sh



SOURCEDIR="wikidata"

if [ ! -d "$SOURCEDIR" ]; then
  mkdir -p $SOURCEDIR
fi

cd $SOURCEDIR

if [ ! -f "$SOURCEDIR/latest-all.nt.gz" ]; then
	echo "Downloading $1"
	wget https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.nt.gz;
fi

cd ..
