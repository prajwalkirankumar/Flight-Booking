import wikipedia,os

import sys
sys.path.append('/Users/prajwalkirankumar/Documents/WT2/api/Chatbot/')

from chatbot import Chat,reflections,multiFunctionCall

import warnings
warnings.filterwarnings("ignore")

def whoIs(query,sessionID="general"):
    try:
        return wikipedia.summary(query)
    except:
        for newquery in wikipedia.search(query):
            try:
                return wikipedia.summary(newquery)
            except:
                pass
    return "I don't know about "+query
        
    

call = multiFunctionCall({"whoIs":whoIs})
firstQuestion="Hi, how are you?"
chat = Chat(os.path.join(os.path.dirname(os.path.abspath(__file__)),"Example.template"), reflections,call=call)
chat.converse_http(firstQuestion)
chat.converse_http(firstQuestion)
chat.converse_http(firstQuestion)
chat.converse_http(firstQuestion)
chat.converse_http(firstQuestion)
chat.converse_http(firstQuestion)

#chat.save_template("test.template")
