from pymongo import MongoClient

# 🔗 MongoDB Connection
MONGO_URI = "mongodb+srv://gayatri_ml:gayatri@cluster0.kfwxoqm.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)

db = client["test"]
collection = db["sensordatas"]

# ✅ FETCH LATEST DATA
def fetch_latest():
    data = collection.find_one(sort=[("_id", -1)])

    if data:
        data["_id"] = str(data["_id"])
        print("✅ Data fetched successfully:\n")
        print(data)
    else:
        print("❌ No data found in collection")

# RUN
if __name__ == "__main__":
    fetch_latest()