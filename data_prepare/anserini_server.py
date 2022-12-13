import argparse
import copy
import traceback
from flask import Flask, json, request, Response
from flask_restful import Resource, Api
from pprint import pprint
import time
import os,json,uuid
from werkzeug.utils import secure_filename
import re
from pyserini.index.lucene import IndexReader
from flask_cors import CORS
import requests

app = Flask(__name__,static_folder='dist')
api = Api(app)

UPLOAD_FOLDER = 'upload'
DOWNLOAD_FOLDER = 'download'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER ):
  os.makedirs(UPLOAD_FOLDER )
if not os.path.exists(DOWNLOAD_FOLDER):
  os.makedirs(DOWNLOAD_FOLDER)


base_response = {
    "status": "FAIL",
    "error": "",
    "text": '',
    # "entities": {},
    "triples": []
}
sentence_seps=['。','！','？','\n']
# sentence_seps_str = '(?<=['+''.join([re.escape(x) for x in sentence_seps])+']).*？'
sentence_seps_str = '['+''.join([re.escape(x) for x in sentence_seps])+']'

def save_file(proj_name,file,fid):
    os.makedirs(os.path.join(UPLOAD_FOLDER,proj_name),exist_ok=True)
    os.makedirs(os.path.join(DOWNLOAD_FOLDER,proj_name),exist_ok=True)
    filename = secure_filename(file.filename)
    filename_spilt = filename.split('.', 1)
    # chinese chars will be removed by secure_filename(), error check
    if len(filename_spilt) == 1:
        filename_spilt = ['_'] + filename_spilt
    # generate unique file name
    filename = filename_spilt[0] + "_" + str(fid) + '.' + filename_spilt[1]
    # save to upload folder
    upload_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
    file.save(upload_path)
    return filename, upload_path

def parse_args():
    parser = argparse.ArgumentParser("triple_extraction_server")
    parser.add_argument("--server_ip", help="Server IP to use", type=str, default="0.0.0.0")
    parser.add_argument("--server_port", help="Server port to use", type=int, default=8830)
    parser.add_argument("--mode", help="Server", type=str, default='cpu')

    return parser.parse_args()


class ExtractionService(Resource):
    def post(self):
        code = 1
        code_message = "Fail!"
        docs = {}
        try:
            if request.json:
                data = request.json
                print(data['ids'])
                for id in data['ids']:
                    doc = MODEL.doc(id)
                    if doc:
                        doc = doc.raw()
                        doc = json.loads(doc)
                        doc = doc['passage']
                        docs[id] = doc
                    else:
                        docs[id] = "Not Found"
                code_message = "Success"
                code = 0
                # return Response(json.dumps(rst, ensure_ascii=False), mimetype="application/json;charset=utf-8")
            else:
                code_message = 'Not Supported'
            rst = {"code":code, "code_message":code_message, "result": docs}
            print(rst)
            return Response(json.dumps(rst, ensure_ascii=False) , mimetype="application/json;charset=utf-8", headers=[("Access-Control-Allow-Origin","*")])
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(e)
            rst = {"code": code, "code_message": code_message, "result": docs}
            return Response(json.dumps(rst, ensure_ascii=False) , mimetype="application/json;charset=utf-8", headers=[("Access-Control-Allow-Origin","*")])

class wikidataEngine(Resource):
    def post(self):

        try:
            if request.form:
                headers = {
                    'Accept': 'application/sparql-results+json',
                    'Content-type': 'application/x-www-form-urlencoded'
                }
                pload = request.form.keys()
                print(pload)
                print('http://ming-gpu-3.cs.uwaterloo.ca:7001')
                r = requests.post('http://ming-gpu-3.cs.uwaterloo.ca:7001', data=pload, headers=headers)
                print(r.content)
                code = 1
                code_message = "Fail!"
                docs = {}
            else:
                code_message = 'Not Supported'
            rst = {"code":code, "code_message":code_message, "result": docs}
            print(rst)
            return Response(json.dumps(rst, ensure_ascii=False) , mimetype="application/json;charset=utf-8", headers=[("Access-Control-Allow-Origin","*")])
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(e)
            rst = {"code": code, "code_message": code_message, "result": docs}
            return Response(json.dumps(rst, ensure_ascii=False) , mimetype="application/json;charset=utf-8", headers=[("Access-Control-Allow-Origin","*")])


def start_server():
    print("Server starting..")

    app = Flask(__name__)
    api = Api(app)
    CORS(app)

    api.add_resource(ExtractionService, "/doc")
    # api.add_resource(wikidataEngine, "/wikidata")

    # app.run(host=args.server_ip, port=args.server_port, threaded=True, ssl_context=('cert.pem', 'key.pem'))
    app.run(host=args.server_ip, port=args.server_port, threaded=True)


if __name__ == "__main__":
    args = parse_args()

    # Initialize from an index path:
#     MODEL = IndexReader('anserini/indexes/lucene-index.msmarco-v2-passage/_novec')
    MODEL = LuceneSearcher.from_prebuilt_index('msmarco-v2-passage')
    print(MODEL.doc('msmarco_passage_18_125506535').raw())

    start_server()
