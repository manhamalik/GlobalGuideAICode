from flask import Flask, render_template, request, session, jsonify
from pymongo import MongoClient
import spacy
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "ahhh"

client = MongoClient(
  "mongodb+srv://manhamalik77:caetoajrTDGWVVLw@cluster0.nfij68g.mongodb.net/?retryWrites=true&w=majority"
)
db = client["TravelBot"]
collection = db["Tinfo"]
nlp = spacy.load("en_core_web_sm")

@app.route('/')
def index():
  # Clear chat history on page refresh
  session['chat_history'] = []

  # Add initial message
  initial_message = "Where would you like to travel first? Please enter a city."
  append_chatbot_message(initial_message) 
  return render_template('index.html', chat_history=session['chat_history'])

@app.route('/send-message', methods=['POST'])
def send_message():
  user_message = request.form['user_message']
  append_user_message(user_message)

  # Get the latest chatbot message to determine the context
  latest_chatbot_message = session['chat_history'][-1][1]
  chatbot_reply = get_information(user_message, latest_chatbot_message)
  append_chatbot_message(chatbot_reply)

  if chatbot_reply == "Would you like to learn more about the hotels, restaurants, attractions, or shopping centers?":
    # Prompt the user to choose the category
    append_chatbot_message(
      "Please choose one of the following categories: hotels, restaurants, attractions, shopping centers."
    )
  # if latest_chatbot_message.split(' ')[0] == "Hotels":
  #   append_chatbot_message(
  #     "Would you like to learn more aobut a specific hotel? If so, which one?"
  #   )
  return jsonify({'reply': chatbot_reply})

def append_user_message(message):
  if 'chat_history' not in session:
    session['chat_history'].append(('user', message))

def append_chatbot_message(message):
  session['chat_history'].append(('chatbot', message))

def get_information(user_input, chatbot_message):
  doc = nlp(user_input)
  keywords = [token.text.lower() for token in doc]

  if any(keyword in keywords for keyword in [
      "paris", "dubai", "toronto", "tokyo", "turkey", "melbourne", "london",
      "nyc", "rome"
  ]):
    if "paris" in keywords:
      document_id = "649728555b26e6f2f08a3408"
    elif "dubai" in keywords:
      document_id = "6497285788e1ead93945cb9e"
    elif "toronto" in keywords:
      document_id = "64a4514d701e25498e080b92"
    elif "tokyo" in keywords:
      document_id = "64a451df766aed3dc2226714"
    elif "turkey" in keywords:
      document_id = "64a4554b8d3af87e86169d67"
    elif "melbourne" in keywords:
      document_id = "64ab802f6e26def1c75f4cbd"
    elif "london" in keywords:
      document_id = "64ab87936e26def1c75f4cbe"
    elif "nyc" in keywords:
      document_id = "64ab90666e26def1c75f4cbf"
    elif "rome" in keywords:
      document_id = "64ab9a376e26def1c75f4cc0"

    session['document_id'] = document_id

    
    
    return "Would you like to learn more about the hotels, restaurants, attractions, or shopping centers?"


 # Check if the chatbot has prompted the user to choose a category
  if chatbot_message == "Please choose one of the following categories: hotels, restaurants, attractions, shopping centers.":
    document_id = session.get('document_id')
    if document_id:
      document = collection.find_one({"_id": ObjectId(document_id)})

      if document:
        # Retrieve specific fields based on user's input
        output = []
        if any(keyword in keywords for keyword in ["thank", "thanks"]):
          output.append("You're welcome! Please let me know if there's anything more I can help you with.")
          
        if any(keyword in keywords for keyword in ["okay", "cool"]):
          output.append("Great, please let me know if there's anything more I can help you with.") 
       
        # For all of the hotels in that city
        if any(keyword in keywords for keyword in ["hotels"]):
          hotels = document.get("hotels")
          if hotels:
            output.append("Hotels: \n" + hotels + "\n\nWould you like to learn more about a specific hotel? If so, which one?")

        # For all of the restaurants in that city
        if any(keyword in keywords for keyword in ["restaurant", "restaurants", "resturant"]):
          restaurants = document.get("restaurants")
          if restaurants:
            output.append("Restaurants: \n" + restaurants + "\n\nWould you like to learn more about a specific restaurant? If so, which one?")

        # For all of the attractions in that city
        if any(keyword in keywords for keyword in ["attraction", "attractions", "attraction"]):
          attraction = document.get("attractions")
          if attraction:
            output.append("Attractions: \n" + attraction + "\n\nWould you like to learn more about a specific attraction? If so, which one?")

        # For all of the shopping centers in that city
        if any(keyword in keywords for keyword in ["shopping", "centers", "center"]):
          shopping = document.get("shopping")
          if shopping:
            output.append("Shopping Centers: \n" + shopping + "\n\nWould you like to learn more about a specific shopping center? If so, which one?")

      #hotel 1 links
        if any(keyword in keywords for keyword in ["ritz", "burj", "langham", "savoy", "hassler", "peninsula"]):
          links = document.get("hotel1_links")
          if links:
            output.append(links)
            
        #hotel 2 links
        if any(keyword in keywords for keyword in ["four", "seasons" "carlton", "pera", "sultanahmet", "atlantis", "palm", "shangri", "crown", "regis"]):
          links = document.get("hotel2_links")
          if links:
            output.append(links)
          
        #hotel 3 links
        if any(keyword in keywords for keyword in ["plaza", "athénée", "athenee", "jumeirah", "beach", "la", "petite", "maison", "fairmont", "royal", "york", "park", "hyatt", "new", "ciragan", "kempinski", "cricket", "ground", "mcg", "claridge", "claridges", "claridge's", "st.", "regis"]):
          links = document.get("hotel3_links")
          if links:
            output.append(links)

        #hotel 4 links
        if any(keyword in keywords for keyword in ["meurice", "armani", "byblos", "otani", "westin", "dorchester", "mandarin", "oriental", "rome", "cavalieri", "waldorf", "astoria", "hazelton"]):
          links = document.get("hotel4_links")
          if links:
            output.append(links)

        
         #restaurant 1 links
        if any(keyword in keywords for keyword in ["l'ambroisie", "ambroisie", "pierchic", "canoe", "sukiyabashi" "jiro", "mikla", "attica", "ledbury", "per", "se", "pergola"]):
          links = document.get("restaurant1_links")
          if links:
            output.append(links)
      
        #restaurant 2 links
        if any(keyword in keywords for keyword in ["epicure", "zuma", "scaramouche", "ryugin", "ciya", "sofrasi" "vue", "Monde", "sketch", "eleven", "madison", "park", "roscioli"]):
          links = document.get("restaurant2_links")
          if links:
            output.append(links)

        #restaurant 3 links
        if any(keyword in keywords for keyword in ["septime", "petite", "maison", "alo", "sushi", "saito", "asitane", "chin", "wolseley", "bernardin", "trattoria", "da", "danilo"]):
          links = document.get("restaurant3_links")
          if links:
            output.append(links)

        #restaurant 4 links
        if any(keyword in keywords for keyword in [ "peti", "jules", "verne", "mosphere", "byblos", "sunset", "grill", "bar", "cumulus", "Inc.", "dinner", "heston", "blumenthal", "peter", "luger", "steak", "armando", "al", "pantheon"]):
          links = document.get("restaurant4_links")
          if links:
            output.append(links)
              
        #attraction 1 links
        if any(keyword in keywords for keyword in ["eiffel", "tower", "burj", "khalifa", "cn", "galatia", "federation", "square", "times", "colosseum"]):
          links = document.get("attraction1_links")
          if links:
            output.append(links)
            
        #attraction 2 links
        if any(keyword in keywords for keyword in ["louvre", "museum", "royal", "ontario", "palm", "jumeirah", "meiji", "shrine", "hagia", "sophia", "royal", "botanic", "gardens", "british", "central", "park", "vatican"]):
          links = document.get("attraction2_links")
          if links:
            output.append(links)
          
        #attraction 3 links
        if any(keyword in keywords for keyword in ["notre", "dame", "cathedral", "dubai", "creek", "ripley's", "ripleys", "aquarium", "disneyland","blue", "mosque", "melbourne", "cricket", "ground", "mcg", "eye", "statue", "liberty", "pantheon"]):
          links = document.get("attraction3_links")
          if links:
            output.append(links)

        #attraction 4 links
        if any(keyword in keywords for keyword in ["arc", "triumph", "islands", "imperial", "palace", "topkapi", "gallery", "victoria", "buckingham", "empire", "state", "building", "trevi", "fountain"]):
          links = document.get("attraction4_links")
          if links:
            output.append(links)

         #shopping 1 links
        if any(keyword in keywords for keyword in ["galeries", "lafayette", "emirates", "eaton", "ginza", "six", "istinye", "zorlu", "Chadstone", "harrods", "fifth", "avenue" ,"galleria", "alberto", "sordi"]):
            links = document.get("shopping1_links")
            if links:
              output.append(links)

        #shopping 2 links
        if any(keyword in keywords for keyword in ["bon", "marche", "dubai", "mall", "yorkville", "village", "shibuya", "109", "zorlu", "melbourne", "selfridges", "brookfield", "place", "Condotti"]):
          links = document.get("shopping2_links")
          if links:
            output.append(links)

        #shopping 3 links
        if any(keyword in keywords for keyword in ["printemps", "haussmann","ibn", "battuta", "cf", "eaton", "centre","omotesanda", "hills", "kanyon", "queen", "victoria", "covent", "hudson", "yards", "del", "corso"]):
          links = document.get("shopping3_links")
          if links:
            output.append(links)

        #shopping 4 links
        if any(keyword in keywords for keyword in ["rue", "faubourg", "saint", "honore", "deira", "yorkdale", "tokyo", "midtown", "vialand", "emporium", "westfield", "london", "brooklyn", "flea", "market", "porta", "portese"]):
          links = document.get("shopping4_links")
          if links:
            output.append(links)

        if output:
          return "\n".join(output)
        else:
          return "Sorry, I couldn't find any information for that category."



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81, debug=True)
