from pymongo import MongoClient

# Your MongoDB connection string
MONGO_URI = "mongodb+srv://gayatri_ml:gayatri@cluster0.kfwxoqm.mongodb.net/?appName=Cluster0"

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Select database and collection
db = client["test"]
collection = db["sensordatas"]

# Function to fetch data
def get_latest_data():
    data = collection.find_one(sort=[("_id", -1)])

    if data:
        data["_id"] = str(data["_id"])

    return data