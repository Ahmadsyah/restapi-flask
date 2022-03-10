# import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

# inisiasi object flask
app = Flask(__name__)

# inisiasi object flask_restful
api = Api(app)

# inisiasi object CORS
CORS(app)

# inisialisasi objek sqlalchemy
db = SQLAlchemy(app)

# mengkofigurasi database
basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database

# membuat database model
class ModelDatabase(db.Model):
    # membuat field / colom
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    umur = db.Column(db.Integer)
    alamat = db.Column(db.TEXT)

    # methode utk menyimpan data
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False


# membuat database
db.create_all()

# inisiasi file kosong bertype dictionary
identitas = {}  # variabel global, dictonary = json

# membuat class resource
class ContohResource(Resource):
    # metode get dan post
    def get(self):
        # menampilkan data dari database
        query = ModelDatabase.query.all()

        # melakukan iterasi pada data model
        output = [
            {
                "id": data.id,
                "nama": data.nama,
                "umur": data.umur,
                "alamat": data.alamat
            }
            for data in query
        ]

        response = {
            "code": 200,
            "msg": "Query data sukses",
            "data": output,

        }
        return response, 200

# insert data ke dalam database model
    def post(self):
        dataNama = request.form["nama"]
        dataUmur = request.form["umur"]
        dataAlamat = request.form["alamat"]

        
        model = ModelDatabase(nama=dataNama, umur=dataUmur, alamat=dataAlamat)
        model.save()

        response = {"msg": "Data berhasil dimasukan", "code": 200}
        return response, 200

# membuat class baru untuk mengedit / menghapus data
class UpdateResourch(Resource):
    def put(self, id):
        # konsumsi id untuk query di database
        # pilih data yang ingin diedit berdasarkan id yang dimasukan
        query = ModelDatabase.query.get(id)

        # form untuk edit data
        editNama = request.form["nama"]
        editUmur = request.form["umur"]
        editAlamat = request.form["alamat"]

        # mereplace nilai yang ada di setiap field/kolom
        query.nama = editNama
        query.umur = editUmur
        query.alamat = editAlamat
        db.session.commit()
        response = {
            "msg" : "Edit data berhasil",
            "code" : 200
        }
        return response

# menghapus data by id
    def delete(self, id):
        queryDelete = ModelDatabase.query.get(id)

        # panggil data untuk delete data by id
        db.session.delete(queryDelete)
        db.session.commit()

        response = {
            "msg" : "Data berhasil dihapus",
            "code" : 200
        }
        return response

# setup resourcenya
api.add_resource(ContohResource, "/api", methods=["GET", "POST"])
api.add_resource(UpdateResourch, "/api/<id>", methods=["PUT", "DELETE"])

if __name__ == "__main__":
    app.run(debug=True, port=5005)
