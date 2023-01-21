
import openai
import pyperclip

from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *
from pywebio import config
############
from pywebio.platform.flask import webio_view
from flask import Flask

app = Flask(__name__)
############
import pywebio
openai.api_key = "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"
mytheme=""

codee=1
ALL_THEME=["sketchy","yeti","minty","default"]
def home():
  # run_js('document.getElementsByClassName("footer").innerHTML="Done by Vijay";console.log(document.body.getElementsByTagName("*"))')
  
  put_image('https://upload.wikimedia.org/wikipedia/commons/4/4d/OpenAI_Logo.svg',width='50%',height='50%').style("display: block;margin-left: auto;margin-right: auto;")
  
  theme = eval_js("new URLSearchParams(window.location.search).get('app')")
  if theme not in ALL_THEME:
      theme = 'default'

  
  put_markdown('# Switch Theme').style("font-size:19px !important;")
  name1=ALL_THEME[0]
  name2=ALL_THEME[1]
  name3=ALL_THEME[2]
  name4=ALL_THEME[3]
  if info.user_agent.is_mobile:
      put_table([[put_button("{}".format(name1),color="dark",onclick=lambda:(go_app(name=name1,new_window=False))),
                  put_button("{}".format(name2),color="dark",onclick=lambda:(go_app(name=name2,new_window=False)))], 
                  [put_button("{}".format(name3),color="dark",onclick=lambda:(go_app(name=name3,new_window=False))),
                  put_button("{}".format(name4),color="dark",onclick=lambda:(go_app(name=name4,new_window=False)))]])
      
  else:
      
      put_table([[put_button("{}".format(name1),color="dark",onclick=lambda:(go_app(name=name1,new_window=False))),
                  put_button("{}".format(name2),color="dark",onclick=lambda:(go_app(name=name2,new_window=False))),
                  put_button("{}".format(name3),color="dark",onclick=lambda:(go_app(name=name3,new_window=False))),
                  put_button("{}".format(name4),color="dark",onclick=lambda:(go_app(name=name4,new_window=False)))]])
  
  
  
  # mytheme=input("Select Theme:",type=TEXT,datalist=["sketchy","yeti","minty","default"])
  put_link("Developed by Vijay",url="http://www.linkedin.com/in/vijay-reddy-160mv",new_window=True,).style("position: absolute;margin-top:75vh;padding:10px;text-align:center;")
  put_link("Github",url="https://www.google.com/",new_window=True,).style("position: absolute;margin-top:75vh;padding:10px;text-align:center;margin-left:50vw;")
  evenorodd()
  

 
def evenorodd():
    engines_dict={"text-davinci-003":3200, "code-davinci-002":2000,"DALL-E (preview)":100}
    myinp=input_group("ASK GPT-3",[
      input("", placeholder='Enter any question', required=True,help_text="For general purpose use \"text-davinci-003\" & for code purposes select \"code-davinci-002\" & for images use \"DALL-E\"",name="question"),
    radio("Choose an engine",name="engine", options=["text-davinci-003", "code-davinci-002","DALL-E (preview)"],required=True)])
    put_text(myinp["question"],).style('color: green; font-size: 20px;font-weight: 600; padding-top:20px')
    put_button("copy",onclick=lambda:(toast("Copied"),pyperclip.copy(response.choices[0].text)),color='success',outline=True).style('float: right')
    if(myinp["engine"]=="DALL-E (preview)"):
        with put_loading(shape='grow',color='success'):
            response = openai.Image.create(
              prompt=myinp["question"],
              n=1,
              size="512x512"
            )
            image_url = response['data'][0]['url'] 
            put_image(response['data'][0]['url']).style("display: block;margin-left: auto;margin-right: auto; padding:20px")
    else:
        with put_loading(shape='grow',color='success'):
            response = openai.Completion.create(
              engine=myinp["engine"],
              prompt=myinp["question"],
              temperature=0.75,
              max_tokens=engines_dict[myinp["engine"]],
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0
            )   
            toast("Success")  
        if("code" in myinp["question"].lower() or myinp["engine"]=="code-davinci-002" or "script" in myinp["question"].lower()):
          global codee  
          put_button("copy",onclick=lambda:(toast("Copied"),pyperclip.copy(response.choices[0].text)),color='success',outline=True).style('float: right')
          if("java" in myinp["question"].lower()):
            put_textarea('Code-Edit'+(str(codee)), code={
              'mode': "Java",
              'theme':'dracula',
            }, value=response.choices[0].text,readonly=True,rows=(int(response.usage.total_tokens)//8))
          elif("python" in myinp["question"].lower()):
            put_textarea('Code-Edit'+(str(codee)), code={
              'mode': "Python",
              'theme':'dracula',
            }, value=response.choices[0].text,readonly=True,rows=(int(response.usage.total_tokens)//8))
          else:
            put_textarea('Code-Edit'+(str(codee)), code={
              'mode': "Java",
              'theme':'dracula',
            }, value=response.choices[0].text,readonly=True,rows=(int(response.usage.total_tokens)//8))
    
          
          
          codee+=1
        else:
          put_button("copy",onclick=lambda:(toast("Copied"),pyperclip.copy(response.choices[0].text)),color='success',outline=True).style('float: right')
          put_text(response.choices[0].text).style('background-color: rgb(240, 240, 240);padding: 10px;border-radius: 8px;')

    put_button("Ask another Question",onclick=evenorodd).style('position: relative;bottom: 0') 
    return("This is the VJ")
    
def dalle2():
    put_text("Hello")
main = {
    theme: config(theme=theme, title=f"PyWebIO {theme} theme")(home) for theme in ALL_THEME if theme != 'default'
}
main['index'] = home
# pywebio.start_server(main,port=8080, debug=True)
app.add_url_rule('/', 'webio_view', webio_view(main),
            methods=['GET', 'POST', 'OPTIONS'])  # need GET,POST and OPTIONS methods
if __name__ == "__main__":
  app.run( port=80)

#inheroku
# pywebio.start_server(home,port=8080,websocket_ping_interval=30)
