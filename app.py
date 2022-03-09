# import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

# inisiasi object flask
app = Flask(__name__)

# inisiasi object flask_restful
api = Api(app)

# inisiasi object CORS
CORS(app)

# inisiasi file kosong bertype dictionary
identitas = {} # variabel global, dictonary = json

# membuat class resource 
class ContohResource(Resource):
    # metode get dan post
    def get(self):
        # response = {"msg" : "hallo dunia, ini resful pertamaku"}
        return identitas

    def post(self):
         nama = request.form["nama"]
         umur = request.form["umur"]
         identitas["nama"] = nama
         identitas["umur"] = umur
         response = {"msg" : "data berhasil dimasukan"}
         return response

# setup resourcenya
api.add_resource(ContohResource, "/api", methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=True, port=5005)


