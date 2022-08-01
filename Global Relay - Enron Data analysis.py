import os
import pandas as pd
import email
from email.parser import Parser
import numpy as np
import re

text = "Message-ID: <18599553.1075842495069.JavaMail.evans@thyme>\nDate: Thu, 10 Feb 2000 03:29:00 -0800 (PST)\nFrom: drew.fossum@enron.com\nTo: bill.cordes@enron.com, dave.neubauer@enron.com, steven.harris@enron.com\nSubject: LRC Joint Venture\nMime-Version: 1.0\nContent-Type: text/plain; charset=us-ascii\nContent-Transfer-Encoding: 7bit\nX-From: Drew Fossum\nX-To: Bill Cordes, Dave Neubauer, Steven Harris\nX-cc: \nX-bcc: \nX-Folder: \\Drew_Fossum_Dec2000_June2001_1\\Notes Folders\\Sent\nX-Origin: FOSSUM-D\nX-FileName: dfossum.nsf\n\nI don't see any problem with this transaction since it appears to be limited \nto Louisiana assets, but the issue of whether we are impacted by the \nnoncompete agreement strikes me as a commercial call. Please let me know if \nyou have any problem with the transaction and I will pursue it. Thanks. DF \n---------------------- Forwarded by Drew Fossum/ET&S/Enron on 02/10/2000 \n11:25 AM ---------------------------\n\n\n\nMichael Moran\n02/09/2000 01:58 PM\nTo: Louis Soldano/ET&S/Enron@ENRON, Dorothy McCoppin/FGT/Enron@ENRON, Phil \nLowry/OTS/Enron@ENRON\ncc: \n\nSubject: LRC Joint Venture\n\nPlease see the attached and let me know if you have any problems so that GPG \ncan respond to Brian Redmond."


dict_1 = {
"Email" : "Message-ID: <18599553.1075842495069.JavaMail.evans@thyme>\nDate: Thu, 10 Feb 2000 03:29:00 -0800 (PST)\nFrom: drew.fossum@enron.com\nTo: bill.cordes@enron.com, dave.neubauer@enron.com, steven.harris@enron.com\nSubject: LRC Joint Venture\nMime-Version: 1.0\nContent-Type: text/plain; charset=us-ascii\nContent-Transfer-Encoding: 7bit\nX-From: Drew Fossum\nX-To: Bill Cordes, Dave Neubauer, Steven Harris\nX-cc: \nX-bcc: \nX-Folder: \\Drew_Fossum_Dec2000_June2001_1\\Notes Folders\\Sent\nX-Origin: FOSSUM-D\nX-FileName: dfossum.nsf\n\nI don't see any problem with this transaction since it appears to be limited \nto Louisiana assets, but the issue of whether we are impacted by the \nnoncompete agreement strikes me as a commercial call. Please let me know if \nyou have any problem with the transaction and I will pursue it. Thanks. DF \n---------------------- Forwarded by Drew Fossum/ET&S/Enron on 02/10/2000 \n11:25 AM ---------------------------\n\n\n\nMichael Moran\n02/09/2000 01:58 PM\nTo: Louis Soldano/ET&S/Enron@ENRON, Dorothy McCoppin/FGT/Enron@ENRON, Phil \nLowry/OTS/Enron@ENRON\ncc: \n\nSubject: LRC Joint Venture\n\nPlease see the attached and let me know if you have any problems so that GPG \ncan respond to Brian Redmond."
}



msg = email.message_from_string(dict_1["Email"]) 

email_body = msg.get_payload()
email_body = re.sub(r'http\S+', 'WEBSITE.', email_body)
email_body = re.sub(r' +', ' ', email_body)
email_body = email_body.replace("\n","")
email_body = email_body.replace("\t","")
email_body = email_body.replace("\'","")


pattern = re.compile(r"^(.*?)-{5,}.*$")
if pattern.findall(email_body):
    email_body = pattern.findall(email_body)[0]

pattern = re.compile(r"^(.*?)={5,}.*$")
if pattern.findall(email_body):
    email_body = pattern.findall(email_body)[0]

pattern = re.compile(r"^(.*?)\*{5,}.*$")
if pattern.findall(email_body):
    email_body = pattern.findall(email_body)[0]



if len([x for x in [" enron "," enron.",".enron "] if x in msg.get_payload().lower()])>0:
    print("True")

from nltk.sentiment.vader import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
sentiment = sia.polarity_scores(email_body)
if sentiment["pos"]>0.5:
    print("positive")
elif sentiment["neg"]>0.5:
    print("negative")
else:
    print("neutral")