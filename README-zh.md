# 線性代訴
_會 RAG 的 LLM Line 聊天機器人_

### 類別
* 本專案在做什麼？
* 演示
* 先決條件
* 設定 Line 開發者帳戶

![人機對話 gif](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/Linear%20algebot.gif)

### 本專案在做什麼？
#### 在終端機或 Jupyter Notebook 環境（例如 Google Colaboratory）中建立一個具有 RAG 能力的 Line 聊天機器人

想用 [Line](https://www.line.me/en/) 自動化客服嗎？
本專案會建立一個具有 RAG（Retrieval-Augmented Generation）能力的聊天機器人，並將其連接到 [LINE](https://www.line.me/en/)  
_Line 是東亞流行的通訊軟體_  

當客戶向您發送訊息時，機器人會自動根據您提供的知識來回覆（即 RAG）

### 演示
您可以用不同的語言向機器人提問：
![與 Linear 聊天機器人對話](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/demo/chat_demo_host.png)
如果遇到它不知道的、或敏感內容，機器人不會直接回答
![隱私保護和避免幻覺](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/demo/chat_demo_host0.png)

### 先決條件
* 當然，需要有網路連線
* 一個 Line 開發者帳戶 **和** 一個 Line 帳戶
  辦帳免費，如果您還沒有帳戶，可以前往 [這裡](https://developers.line.biz/en/) 建立一個新帳戶
* Linux shell 或 Jupyter Notebook 環境
_Jupyter Notebook 是一個開源的多語言程式開發介面_
例如：
    * [MyBinder](https://mybinder.org/)
      _由非營利組織維運_
    * [Google Colaboratory](https://colab.research.google.com/)（即 colab）
      _記得開啟 GPU 執行階段_
    * [本地主機使用 Anaconda](https://www.anaconda.com/download)
    * [本地主機使用 VS code](https://code.visualstudio.com/)
    * [本地主機使用 Jupyter](https://jupyter.org/install)
##### 注意：如果有 GPU，建議在 GPU 環境執行此專案，否則推理會曠日費時

### 設定 Line 開發者帳戶
#### _如果已建好 Line 開發者帳戶，可略過此部分_
1. 前往 [Line 開發者網站](https://developers.line.biz/zh-hant/)
2. 點擊 `Login to console` 並選擇您的登入方式（或建立一個帳戶，需要手機號碼）
![Line 首頁](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/home_page_tw.png)
![Line 登入頁面](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/login_tw.png)
3. 點擊 `create provider`，然後 `create a new channel`，選擇 `Messaging API`
![建立提供者](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/click_provider.png)
![建立新頻道](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/create_channel.png)
![選擇訊息 API](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/choose_msg_api.png)
4. 填寫所需的欄位 ~~使用假資訊~~
5. 打開頻道管理員或返回儀表板，然後點擊 `provider > 您建立的頻道`
![選擇您剛建立的提供者](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/click_provider.png)
![然後選擇頻道](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/click_channel.png)
6. 向下捲動並複製密鑰，將其貼到 `config.py`（YOUR_CHANNEL_SECRET 部分）
![發布或複製您的密鑰](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/channel_secret.png)
7. 點擊 Messaging API
    * 可透過 ID 或掃描二維碼將機器人加入好友
    ![點擊訊息 API](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/click_messaging_API.png)
    ![與您的機器人成為好友](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/add_your_bot.png)
    * 向下捲動，啟用 webhook
    _當事件發生（例如客戶發送訊息），Line 會向 webhook URL (即您的機器人) 發送請求_
    ![點擊「使用 webhook」按鈕](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/enable_webhook.png)
    * 至於 `Webhook URL`，稍後再料理它
8. 再向下捲動，發布/重新發布 `Channel access token`，然後將其複製並貼到 `config.py`（YOUR_CHANNEL_ACCESS_TOKEN 部分）
![發布並獲取您的頻道存取令牌](https://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/line_account/issue_channel_token.png)
#### 注意：別讓他人知道密鑰和存取令牌

### Jupyter 解決方案
只需按照 [這個筆記本](hhttps://codeberg.org/Codeglacier/Linear_Algebot/raw/branch/main/chatbot_zh.ipynb) 說明進行操作

### Shell 解決方案
用 Python Flask 當後端框架  
然而，它預設會架起 `HTTP` 服務，但我們想開的是 `HTTPS` 服務  
本專案中的免費和開源解決方案是：
* localtunnel (lt)
* Tunnelmole (tmole)

#### 複製儲存庫
```bash
git clone https://codeberg.org/Codeglacier/Linear_Algebot.git

cd linear_algebot
```

這個終端將作為聊天機器人服務的後端  
聊天機器人的程式邏輯在 `app.py` 中

#### 安裝依賴項
```bash
pip install -U -r requirements.txt
```

#### 安裝服務暴露模組
_用開源專案替換 ngrok，此處選 tunnelmole 和 localtunnel  
此二者皆可在 Google Colaboratory 和 Linux shell 運作_

```bash
# 安裝 tunnelmole
curl -O https://install.tunnelmole.com/xD345/install && sudo bash install

# 如果您更喜歡 localtunnel，請安裝 localtunnel
# curl https://loca.lt/mytunnelpassword
```

#### 準備暴露服務的埠口
啟動聊天機器人前，須先提供埠口

```bash
# 啟動 tunnelmole 並分配 1989 埠（或您喜歡的任何其他埠）
nohup tmole 1989 &

# nohup lt --port 1989 & # 如果您更喜歡 localtunnel，請使用此命令
```

#### 設定服務的 URL
理論上會自動生成一個名為 'nohup.out' 的文件  
在文件中找到與 localhost 目錄對應的 https 網址，並將其複製到 `app.py` 中的 `prefix_url`

#### **重要！**
複製 URL 並在其末尾加上 `/callback`，然後將整個網址貼到 Line 開發者頁面中的 Webhook URL 欄位
例如 https://your-prefix-url + /callback = https://your-prefix-url/callback

---

#### 啟動聊天機器人應用程序
將網址貼到 Line webhook 和 `app.py` 中的 prefix_url 後，就可以啟動聊天機器人 app 了
```bash
# 再次提醒，執行前請先更新 app.py 中的 prefix_url
python app.py
```

### 可以開始和機器人聊天了！
試試從一般 Line 介面傳訊息給機器人  
如果順利，機器人應會回覆

---

### 終止服務
除點擊 Notebook UI 的停止按鈕來結束服務，別忘記幹掉背景執行的 tunnelmole 或 localtunnel

```bash
# 終止 tunnelmole
pkill -f 'tmole 1989'
# pkill -f 'lt --port 1989' # localtunnel 版本
```

致謝：
* [楊德倫 messaging Linebot repo](https://github.com/telunyang/python_linebot_messaging_api) (未包含 LLM)
* [Tunnelmole](https://tunnelmole.com/docs/)
* [localtunnel](https://github.com/localtunnel/localtunnel)

