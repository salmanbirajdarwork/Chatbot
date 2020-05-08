from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot import logic
from chatterbot import filters
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import json
import os
import glob
import sys

from give_answer_google import answer_question

botApp = Flask(__name__)

####
bot = ChatBot(
    "relocation-assist-chatbot",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///db.sqlite3',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'maximum_similarity_threshold': 0.1
        },
        'chatterbot.logic.MathematicalEvaluation',
        # 'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.UnitConversion',
        'chatterbot.logic.SpecificResponseAdapter'

    ],
    filters=['chatterbot.filters.RepetitiveResponseFilter']
)
trainer = ListTrainer(bot)
trainer = ChatterBotCorpusTrainer(bot)
trainer.train('chatterbot.corpus')

# code for training from text files
path = 'textfiles/'
# for filename in os.listdir(path):
for filename in glob.glob(os.path.join(path, '*.txt')):
    print("fileName : ", filename)
    conv = open(filename, 'r', encoding="utf8", errors='ignore').readlines()
    trainer = ListTrainer(bot)
    trainer.train(conv)

# Code for training from  JSON files
convArray = []
with open('./qa_Health_and_Personal_Care.json') as json_file:
    data = json.load(json_file)
    for p in data['test']:
        convArray.append(p['question'])
        convArray.append(p['answer'])

trainer.train(convArray)

###### PreProcessor ######
def unescape(bot, statement):
    if sys.version_info[0] < 3:
        from HTMLParser import HTMLParser
        html = HTMLParser()
    else:
        import html
        statement.text = html.unescape(statement.text)
        return statement


@botApp.route("/")
def home():
    return render_template("index.html")


@botApp.route("/get")
def get_bot_response():
    userText = request.args.get('msg')

    if not (not (userText.strip() == "Help") and not (userText.strip() == "help")) or (userText.strip() == "Help!"):
        return str('Ok, here is a link to search more: <a href=\'https://www.google.com\'>www.google.com</a>')
    else:
        respo = bot.get_response(userText)
        print("conf",respo.confidence)
        if not respo.confidence > 0.75:
            respo = answer_question(userText)
        print("response: ", respo)
        return str(respo)

if __name__ == "__main__":
    botApp.run()
