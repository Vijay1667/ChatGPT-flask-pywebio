
import openai
import pyperclip

from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *

import pywebio
openai.api_key = "YOUR API KEY"


def home():
  put_image('https://upload.wikimedia.org/wikipedia/commons/4/4d/OpenAI_Logo.svg',width='50%',height='50%')
  evenorodd()
def evenorodd():
    engines_dict={"text-davinci-003":3200, "text-curie-001":1600, "text-babbage-001":1600, "text-ada-001":1600,"code-davinci-002":2000}
    myinp=input_group("ASK GPT-3",[
      input("", placeholder='Enter any question', required=True,help_text="For code purposes select \"code-davinci-002\"",name="question"),
    radio("Choose an engine",name="engine", options=["text-davinci-003", "text-curie-001", "text-babbage-001", "text-ada-001","code-davinci-002"],required=True)])
    put_text(myinp["question"]).style('color: green; font-size: 20px;font-weight: 600; padding-top:20px')

    
    with put_loading(shape='grow',color='success'):
      response = openai.Completion.create(
        engine=myinp["engine"],
        prompt=myinp["question"],
        temperature=0.2,
        max_tokens=engines_dict[myinp["engine"]],
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )   
      toast("Success")  

    
    if("code" in myinp["question"].lower() or myinp["engine"]=="code-davinci-002" or "script" in myinp["question"].lower()):
      put_button("copy",onclick=lambda:(toast("Copied"),pyperclip.copy(response.choices[0].text)),color='success',outline=True).style('float: right')
      put_textarea('Code-Edit', code={
          'mode': "Java",
          'theme':'dracula',
      }, value=response.choices[0].text,readonly=True,rows=(int(response.usage.total_tokens)//10))
    else:
      put_button("copy",onclick=lambda:(toast("Copied"),pyperclip.copy(response.choices[0].text)),color='success',outline=True).style('float: right')
      put_text(response.choices[0].text).style('background-color: rgb(240, 240, 240);padding: 10px;border-radius: 8px;')

    
    
    put_button("Ask another Question",onclick=evenorodd).style('position: relative;bottom: 0') 
    

pywebio.start_server(home,port=90, debug=True)
