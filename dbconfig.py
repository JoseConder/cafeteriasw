from pymongo import MongoClient

password = "mondongo"
dbname = "comida"

uri = f"mongodb+srv://a299506:{password}@cluster0.orzxcsb.mongodb.net/{dbname}?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

#client = MongoClient('localhost', 27017)
db = client['comida']
productos_collection = db['productos']
pedidos_collection = db['pedidos']