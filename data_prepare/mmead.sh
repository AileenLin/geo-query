wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/mmead/msmarco_v2_passage_links_v1.0.tar
tar -zxvf msmarco_v2_passage_links_v1.0.tar
python process_data.py
bash process_rdf.sh
mkdir mmead_indicies
cd mmead_indicies
mv ../msmarco_v2_ttl ./
mv Qleverfile.mmead ../qlever-control/Qleverfiles/
. ../qlever-control/qlever mmead
qlever index
qlever start
