#### Script for downloading DBpedia files and preprocess them
#### Adapted from https://github.com/dice-group/KG-NMT/blob/master/KGE_creation.sh



SOURCEDIR="data"

if [ ! -d "$SOURCEDIR" ]; then
  mkdir -p $SOURCEDIR
fi

cd $SOURCEDIR

if [ ! -f "$SOURCEDIR/instance_types_en.ttl" ]; then
	echo "Downloading $1"
	wget http://downloads.dbpedia.org/2016-10/core-i18n/en/instance_types_en.ttl.bz2;
fi

if [ ! -f "$SOURCEDIR/mappingbased_objects_en.ttl" ]; then
	wget http://downloads.dbpedia.org/2016-10/core-i18n/en/mappingbased_objects_en.ttl.bz2 ;
fi

if [ ! -f "$SOURCEDIR/article_categories_en.ttl" ]; then
	wget http://downloads.dbpedia.org/2016-10/core-i18n/en/article_categories_en.ttl.bz2 ;
fi


echo "Unzipping the files ..."
if [ -f "mappingbased_objects_en.ttl.bz2" ] ; then
	bzip2 -d *.bz2;
fi


echo "Filtering triples: mappingbased_objects"
sed -i '' -e '1d' mappingbased_objects_en.ttl
#sed -i '' -e '/__[0-9]*/d' mappingbased_objects_en.ttl
sed -i '' -e '/http:\/\/dbpedia.org\/ontology\//!d' mappingbased_objects_en.ttl


echo "Filtering triples: instance types"
sed -i '' -e '1d' instance_types_en.ttl
#sed -i '' -e '/__[0-9]*/d' instance_types_en.ttl
sed -i '' -e '/http:\/\/dbpedia.org\/ontology\//!d' instance_types_en.ttl


echo "Filtering triples: article_categories_en"
sed -i '' -e '1d' article_categories_en.ttl
sed -i '' -e 's/http:\/\/purl.org\/dc\/terms\//dc_terms:/g' article_categories_en.ttl


if [ -f "mappingbased_objects_en.ttl" ] ; then
	echo "Merging files into a single..."
	cat *.ttl > triples.nt
fi

echo "Replacing namespaces  ..."
sed -i '' -e 's/http:\/\/dbpedia.org\/resource\//dbr:/g' triples.nt
sed -i '' -e 's/http:\/\/dbpedia.org\/ontology\//dbo:/g' triples.nt
sed -i '' -e 's/http:\/\/www.w3.org\/1999\/02\/22-rdf-syntax-ns#/rdf:/g' triples.nt



cd ..
