# import library
import jwt
import datetime
from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from functools import wraps

# inisialisasi
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = "ini rahasia"

# decorator untuk kunci autentikasi
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        # token akan di parsing dengan parameter di dendpoin
        token = request.args.get('token')
        # cek token
        if not token:
            return make_response(jsonify({"msg":"token tidak ada"}), 404)

        # decode token yang diterima
        try:
            output = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return make_response(jsonify({"msg": "token salah"}))
        return f(*args, **kwargs)
    return decorator

# membuat endpoint untuk login
class LoginUser(Resource):
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')

        # membuat autentikasi password
        if username and password == 'superadmin':
            # hasilkan no token
            token = jwt.encode(
                {
                    "username": username,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
                },  app.config['SECRET_KEY'], algorithm="HS256"
            )
            return jsonify({
                "token": token,
                "msg": "Anda berhasil login !"
                })
        return jsonify({"msg":"silahkan login !"})

# halaman yang harus login
class Dashboard(Resource):
    # menambahkan dekorator untuk mengunci halaman
    @token_required
    def get(self):
        return jsonify({"msg": "ini halaman yang diakses dengan login"})

# halaman tanpa login
class HomePage(Resource):
    def get(self):
        return jsonify({"msg": "ini adalah halaman public"})


api.add_resource(LoginUser, "/api/login", methods=["POST"]) 
api.add_resource(Dashboard, "/api/dashboard", methods=["GET"]) 
api.add_resource(HomePage, "/api", methods=["GET"]) 

if __name__ == "__main__":
    app.run(debug=True)