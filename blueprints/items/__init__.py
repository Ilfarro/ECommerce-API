from flask_restful import fields
from blueprints import db

class Items(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kategori = db.Column(db.String(200))
    nama = db.Column(db.String(200))
    deskripsi = db.Column(db.String(200))
    harga = db.Column(db.Integer)
    lokasi = db.Column(db.String(200))
    url_foto = db.Column(db.String(200))
    post_by = db.Column(db.String(200))

    response_field = {
        'id': fields.Integer,
        'kategori': fields.String,
        'nama': fields.String,
        'deskripsi': fields.String,
        'harga': fields.Integer,
        'lokasi': fields.String,
        'url_foto': fields.String,
        'post_by': fields.String
    }

    def __init__(self, id, kategori, nama, deskripsi, harga, lokasi, url_foto, post_by):
        self.id = id
        self.kategori = kategori
        self.nama = nama
        self.deskripsi = deskripsi
        self.harga = harga
        self.lokasi = lokasi
        self.url_foto = url_foto
        self.post_by = post_by

    def __repr__(self):
        return f'<Items {self.id}>'

db.create_all()