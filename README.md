# Linear Algebot \| [中文版](https://codeberg.org/Codeglacier/Linear_Algebot/src/branch/main/README-zh.md)
_LLM Line chatbot with RAG_

### Category
* What does this project do?
* Demo
* Prerequisite
* Set up a Line Developer account

![Human-bot chatting gif](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/Linear%20algebot.gif)

### What does this project do?
#### building up a Line chatbot with RAG ability in terminal or Jupyter Notebook environment (e.g. Google Colaboratory) 

Want to automate your customer service with [Line](https://www.line.me/en/)?  
This project create a chatbot with RAG (Retrieval Augmented Generation) ability and hook it to [LINE](https://www.line.me/en/), a pupolar text app across Asia.

When customer texts you something, the bot will automatically send a reply based on the knowledge you gave it (i.e. RAG).

### Demo
You can ask the bot with different language:
![QA with Linear chatbot](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/demo/chat_demo_host.png)
If encountering something it doesn't know or sensitive, the bot won't answer directly
![Privacy protection and hallucination avoidance](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/demo/chat_demo_host0.png)

### Prerequisite
* Of couese, Internet
* A Line Developer account **AND** a Line account  
  It's free. You can go [here](https://developers.line.biz/en/) to create a new account if you didn't have one.
* Linux shell or Jupyter Notebook environment  
_Jupyter Notebook is an open source UI interface for multiple programming language development_  
e.g. 
    * [MyBinder](https://mybinder.org/)
      _hosted by a non-profit organisation_
    * [Google Colaboratory](https://colab.research.google.com/) (i.e. colab)
      _Remember to turn GPU runtime on_
    * [Local-host with Anaconda](https://www.anaconda.com/download)
    * [Local-hosting with VS code](https://code.visualstudio.com/)
    * [Local-hosting Jupyter](https://jupyter.org/install) 
##### Note: It's highly recommended to run this project in GPU environment if you have one, otherwise inference would take forever

### Set up a Line Developer account
#### _You can skip this part if you already have a built-up Line dev account_
1. Go to [Line developer website](https://developers.line.biz/en/)
2. Click `Login to console` and choose your way to login (or create an account, which will need a phone number)
![Line home page](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/home_page.png)
![Line login page](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/login.png)
3. Click `create provider`, then `create a new channel`, choosing `Messaging API`
![create provider](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/click_provider.png)
![create a new channel](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/create_channel.png)
![Choosing message API](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/choose_msg_api.png)
4. Filling up the required fields ~~with fake info~~
5. Open the channel manager or go back to the dashboard and click the `provider > the channel you built` after done
![Choose the provider you just created](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/click_provider.png)
![Then choose the channel](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/click_channel.png)
6. scroll down and copy your channel secret, pasting it into `config.py` (YOUR_CHANNEL_SECRET part)
![issuing or copying your channel secret](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/channel_secret.png)
7. Click Messaging API
    * You can add your bot as a friend via ID or scanning the qr-code
    ![click msg API](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/click_messaging_API.png)
    ![friend up with your bot](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/add_your_bot.png)
    * scrolling down, enable the webhook usage
    _When an event takes place (e.g. customer texts you), Line will send a request to webhook url, i.e. your bot_
    ![click 'use webhook' button](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/enable_webhook.png)
    * Don't worry about the `Webhook URL` since we'll cope with it later
8. scroll down further to issue\/reissue a `Channel access token`, then copy-paste it into `config.py` (YOUR_CHANNEL_ACCESS_TOKEN part)
![issue and get your channel access token](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/issue_channel_token.png)
#### Note: don't let others know your channel secret and access token

### Jupyter solution
Just follow the instructions in [this notebook](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/chatbot.ipynb)

### Shell solution
We'll use python Flask as our backend framework.  
However, it will host `HTTP` by default, whereas we like to expose our service to public `HTTPS`  
The free and open source solutions in this project are:
* localtunnel (lt)
* Tunnelmole (tmole)

#### Clone the repository  
```bash
git clone https://codeberg.org/Codeglacier/Linear_Algebot.git

cd linear_algebot
```

This terminal will serve as the backend for chatbot service  
The chatbot logic is in `app.py`

#### Install dependencies
```bash
pip install -U -r requirements.txt
```

#### Install service-exposing module
_To replace ngrok with open source alternatives, I chose tunnelmole and localtunnel.  
They both can work on Google colaboratory and Linux shell._

```bash
# install tunnelmole
curl -O https://install.tunnelmole.com/xD345/install && sudo bash install

# install localtunnel if you prefer it to tunnelmole
# curl https://loca.lt/mytunnelpassword
```

#### Prepare a port for service-exposure
The port has to be served before you run the chatbot app.

```bash
# run tunnelmole in the background and assign port 1989 (or any other port you like)
nohup tmole 1989 & 

# nohup lt --port 1989 & # Use this command if you prefer localtunnel
```

#### Setting up the URL for service
Theoretically, there will be a file called 'nohup.out' generated automatically.  
Find the https address corresponding to your localhost directory within the file, and copy it to `prefix_url` in `app.py`

#### **Important!**
Copy the URL and stick `/callback` to its end before pasting the whole address to the Webhook URL field in Line developer page.  
E.g. https://your-prefix-url \+ /callback = https://your-prefix-url/callback

---

#### Launch the chatbot app
After pasting the address to Line webhook and to prefix_url in app.py, we can finally run the chatbot app.
```bash
# update the prefix_url in app.py before running it
python app.py
```

### You can go texting your bot now!
Try sending some messages through Line client interface  
If everything works smoothly, the bot would reply to you

---

### Service termination
Apart from stopping the app by clicking the stop button in Notebook UI, don't forget to terminate tunnelmole or localtunnel in background execution.

```bash
# terminate the background execution of tunnelmole
pkill -f 'tmole 1989'
# pkill -f 'lt --port 1989' # localtunnel version
```

Credits:
* [楊德倫 messaging Linebot repo](https://github.com/telunyang/python_linebot_messaging_api) (No LLM included)
* [Tunnelmole](https://tunnelmole.com/docs/)
* [localtunnel](https://github.com/localtunnel/localtunnel)





