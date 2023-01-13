import pywebio
from pywebio.input import *
from pywebio.input import input,FLOAT
from pywebio.output import *
from pywebio import *
import os
import openai
import pyperclip
import argparse
from flask import Flask, send_from_directory
from pywebio.platform.flask import webio_view
app=Flask(__name__)
openai.api_key = "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"
def check_openapi():
  if(openai.api_key==""):
    return "OPENAI api key not specified"
  return None  

def home():
  put_image('https://upload.wikimedia.org/wikipedia/commons/4/4d/OpenAI_Logo.svg',width='50%',height='50%')
  evenorodd()
def evenorodd():
    engines_dict={"text-davinci-003":3200, "text-curie-001":1600, "text-babbage-001":1600, "text-ada-001":1600}
    myinp=input_group("ASK GPT-3",[input('', type=TEXT ,placeholder='Enter any question', required=True,help_text="",name="question"),
              radio("Choose an engine",name="engine", options=["text-davinci-003", "text-curie-001", "text-babbage-001", "text-ada-001"],required=True)])
    
    put_text(myinp["question"]).style('color: green; font-size: 20px;font-weight: 600; padding-top:20px')
    with put_loading(shape='grow',color='success'):
      response = openai.Completion.create(
        engine=myinp["engine"],
        prompt=myinp["question"],
        temperature=0.5,
        max_tokens=engines_dict[myinp["engine"]],
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )   
      toast("Success")  

    put_button("copy",onclick=lambda:(toast("Copied"),pyperclip.copy(response.choices[0].text)  ),color='success',outline=True).style('float: right')
    put_text(response.choices[0].text).style('background-color: rgb(240, 240, 240);padding: 10px;border-radius: 8px;')
    put_button("Ask another Question",onclick=evenorodd).style('position: relative;bottom: 0') 
    
     

    

app.add_url_rule('/tool', 'webio_view', webio_view(home),methods=['GET', 'POST', 'OPTIONS'])
   

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(home, port=args.port)

    