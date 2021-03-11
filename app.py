import json
import requests
import versiongetter
import shutil
import os
import tempfile #1
from test import BlobDownloadAuthN,BlobSASUri
from azure.storage.blob import BlobClient
from azure.storage.blob import ContainerClient
from azure.identity import DefaultAzureCredential
from AzureBlobBackend import BlobVersionsGet,BlobVersionsGetAuthN
from flask import Flask, abort,current_app, flash, jsonify, make_response, send_file, redirect#, request, url_for
from os import path


app = Flask(__name__)
azblobstoragehost = "https://terrreggm.blob.core.windows.net"
azcontainer = "terrregistryblob"
#Service Discovery
@app.route('/.well-known/terraform.json', methods=['GET'])
def discovery():
    return {"modules.v1": "/v1/modules/"}

#Get Versions
@app.route('/v1/modules/<namespace>/<name>/<provider>/versions', methods=['GET'])
def versions(namespace, name,provider):
    # filepath = './v1/modules/' + namespace + "/" + name + "/" + provider + "/"
    # if not path.exists(filepath):
    #     abort(404)
    response = BlobVersionsGetAuthN(azblobstoragehost,azcontainer,namespace,name,provider)
    return f'{response}'

#Download Specific Version :namespace/:name/:provider/:version/download
@app.route('/v1/modules/<namespace>/<name>/<provider>/<version>/download', methods=['GET'])
def downloadversion(namespace, name,provider,version):
    blobpath = f'/v1/modules/{namespace}/{name}/{provider}/{version}/local.zip'
    response = make_response('', 204 )
    response.mimetype = current_app.config['JSONIFY_MIMETYPE']
    response.headers['X-Terraform-Get'] = blobpath
    return response
    
#need to actually send the file
@app.route('/v1/modules/<namespace>/<name>/<provider>/<version>/local.zip', methods=['GET'])
def downloadfile(namespace, name,provider,version):
    sasuri = BlobSASUri(azblobstoragehost,'terrreggm',azcontainer, namespace,name,provider,version)
    return redirect(sasuri)