from flask import Flask, render_template
from pymongo import MongoClient
import spacy

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

# Connect to MongoDB
client = MongoClient("mongodb+srv://manhamalik77:caetoajrTDGWVVLw@cluster0.nfij68g.mongodb.net/?retryWrites=true&w=majority")
db = client["TravelBot"]
collection = db["Tinfo"]

def get_information(user_input):
    doc = nlp(user_input)
    keywords = [token.text.lower() for token in doc]

    if any(keyword in keywords for keyword in ["hotel", "hotels"]):
         query = {"category": "hotels"}
    elif any(keyword in keywords for keyword in ["restaurant", "restaurants"]):
         query = {"category": "restaurant"}
    elif any(keyword in keywords for keyword in ["attraction", "attractions"]):
         query = {"category": "attraction"}
    elif any(keyword in keywords for keyword in ["shopping", "centers"]):
         query = {"category": "shopping"}
    else:
         return "I'm sorry blah nlah, please specify what you are looking for hotel, "
    
    result = collection.find_one(query)
    if result:
            return result["message"]
    else:
        return "I'm sorry, I couldn't find any information for your request."


# #Replace <connection_string> with your MongoDB connection string
# client = MongoClient("mongodb+srv://manhamalik77:caetoajrTDGWVVLw@cluster0.nfij68g.mongodb.net/?retryWrites=true&w=majority")

# Access your database and collection
# db = client["TravelBot"]
# collection = db["Tinfo"]

# # Insert a document
# # document = {'name:' "Paris", 'description:' "The capital city of France"}
# document = {
#     "name": "France",
#     "description": "The capital city of France"
# },

# collection.insert_one(document)

# import requests

# def get_public_ip():
#     try:
#         response = requests.get('https://api.ipify.org')
#         if response.status_code == 200:
#             return response.text
#     except requests.RequestException:
#         pass
#     return None

# public_ip = get_public_ip()
# if public_ip:
#     print(f"Public IP Address: {public_ip}")
# else:
#     print("Unable to retrieve the public IP address.")


# result = collection.insert_one(document)

# if result.acknowledged:
#   print("Document inserted successfully.")
# else:
#   print("Failed to insert document.")



# db.movies.insertOne(
#   {
#     title: "The Favourite",
#     genres: [ "Drama", "History" ],
#     runtime: 121,
#     rated: "R",
#     year: 2018,
#     directors: [ "Yorgos Lanthimos" ],
#     cast: [ "Olivia Colman", "Emma Stone", "Rachel Weisz" ],
#     type: "movie"
#   }
# )
app = Flask(__name__)


# @app.route('/')
# def index():
#     return render_template('index.html')


app.run(host='0.0.0.0', port=81, debug=True)

# nlp = spacy.load('en_core_web_sm')
