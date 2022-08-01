import os
import pandas as pd
import email
from email.parser import Parser
import numpy as np
import re



import os
rootdir = "C:\\Users\\StarTrek\\Downloads\\enron_mail_20150507\\maildir\\"

user_pattern = re.compile(r"^C:\\Users\\StarTrek\\Downloads\\enron_mail_20150507\\maildir\\([a-z\-]+)\\.+$")
subdir_pattern = re.compile(r"^C:\\Users\\StarTrek\\Downloads\\enron_mail_20150507\\maildir\\[a-z\-]+\\(.+)\\.+$")
file_pattern = re.compile(r"^C:\\Users\\StarTrek\\Downloads\\enron_mail_20150507\\maildir\\[a-z\-]+\\.+\\(.+)$")
check_pattern = re.compile(r"^C:\\Users\\StarTrek\\Downloads\\enron_mail_20150507\\maildir\\[a-z\-]+\\.+\\.+$")


user = []
subfolder = []
file_no = []
to = []
from_1 = []
subject = []
message = []

i = 1
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        file_path = str(os.path.join(subdir, file))
        i = i+1
        if check_pattern.search(file_path) and i<=100:
            
            user.extend(user_pattern.findall(file_path))
            subfolder.extend(subdir_pattern.findall(file_path))
            file_no.append(file)

            with open(file_path,"r") as email_1:
                text = email_1.read()
            msg = email.message_from_string(text) 
            to.append(msg["To"])
            from_1.append(msg["From"])
            subject.append(msg["Subject"])
            message.append(msg.get_payload())
        if i>100:
            break
    if i>100:
        break
            
df = pd.DataFrame({"user":user, "subfolder":subfolder, "file_no":file_no, 
              "from":from_1,"to":to,"subject":subject,"message":message})
df.shape
df.sort_values(by = ["user","subfolder","file_no"])

df.user.unique()
list(df.to.unique())
list(df["from"].unique())

mail_domain = re.compile(r".+@(.+).com.*")
domain = [mail_domain.findall(x) for x in from_1]
pd.Series(domain).value_counts()



import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

word_corpus = []

for msg_txt in message:
    text_1 = msg_txt
    text_1 = text_1.replace("\n","")
    text_1 = text_1.replace("t","")
    text_1 = text_1.replace("=","")    
    words = word_tokenize(text_1)
    word_corpus.extend(words)

word_corpus = [word for word in word_corpus if word not in stopwords.words('english')]

pd.Series(word_corpus).value_counts()
pd.set_option('display.max_rows', 500)
list(pd.Series(word_corpus).value_counts().index)[0:100]
