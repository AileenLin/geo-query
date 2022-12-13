#!/bin/bash

for filename in ./msmarco_v2_unzipped_slim/*
do
 if [[ `basename $filename` == "msmarco_v2_passage_links_"* ]]; then
   fullfname=`basename $filename`
#    fullfname="${fullfname/"regressions-"/""}"
   fullfname="${fullfname/".json"/""}"
   java -jar json2rdf-jar-with-dependencies.jar http://example.com/test# \
   < $filename \
   >> "./msmarco_v2_ttl/${fullfname}.ttl"
 fi
done;
