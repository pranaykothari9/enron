#https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask

#importing libraries
from flask import Flask, request
from flask_restful import Api
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import email
import re

#setting up flask app
app = Flask(__name__)
api = Api(app)

#receiving input
@app.route('/', methods =["POST"])
def json_input_email():
    request_data = request.get_json()

    #using email library to parse email input
    msg = email.message_from_string(request_data['Email']) 
    
    #extracting email body
    email_body = msg.get_payload()
    
    #processing email body
    email_body = re.sub(r'http\S+', 'WEBSITE.', email_body) #Substituting URL with word 'WEBSITE'
    email_body = re.sub(r' +', ' ', email_body)             #Replacing multiple spaces with single space
    email_body = email_body.replace("\n","")                #Removing \n 
    email_body = email_body.replace("\t","")                #Removing \t
    email_body = email_body.replace("\'","")                #Replacing \' with single quote (') e.g.: That\'s --> That's 
    
    
    #-----Patterns to eliminate trail mails----------
    
    #Pattern 1: multiple hyphens ("-----------------------------")
    pattern = re.compile(r"^(.*?)-{5,}.*$")
    if pattern.findall(email_body):
        email_body = pattern.findall(email_body)[0]
   
    #Pattern 2: multiple equal signs ("========================") 
    pattern = re.compile(r"^(.*?)={5,}.*$")
    if pattern.findall(email_body):
        email_body = pattern.findall(email_body)[0]
    
    #Pattern 3: multiple stars ("***********************")
    pattern = re.compile(r"^(.*?)\*{5,}.*$")
    if pattern.findall(email_body):
        email_body = pattern.findall(email_body)[0]
    
    #initialize output    
    output = {"sentiment":"","enron_flag":False}

    #if word "Enron" found then enron_flag is SET
    if len([x for x in [" enron "," enron.",".enron ", "oil", "gas"] if x in msg.get_payload().lower()])>0:
        output["enron_flag"] = True
    
    #getting sentiment of email
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(email_body)
    if sentiment["pos"]>0.5:
        output["sentiment"] = "positive"
    elif sentiment["neg"]>0.5:
        output["sentiment"] = "negative"
    else:
        output["sentiment"] = "neutral"


    return output
          

if __name__ == '__main__':
    app.run(debug=False)