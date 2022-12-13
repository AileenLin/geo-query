git clone git@github.com:ad-freiburg/qlever-control.git
mkdir wikidata_indicies
cd wikidata_indicies
. ../qlever-control/qlever wikidata
qlever get-data
qlever index
qlever start
