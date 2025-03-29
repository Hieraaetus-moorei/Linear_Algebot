# import flask-related modules
# 載入 flask 相關模組
from flask import Flask, request, abort, send_from_directory

# requests module for server communication
# 載入 requests 模組，用來和伺服器溝通
import requests

# import line bot sdk for python
# 載入 line bot python sdk
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage,
    VideoMessage,
    AudioMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent,
    VideoMessageContent,
    AudioMessageContent
)



#======================== bot's brain ========================#

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
from sentence_transformers import SentenceTransformer, util
import faiss

# reduce the precision for memory and calculation efficiency
# 降低精度以節省記憶體、計算資源
if torch.cuda.is_available():
    bnb_config = BitsAndBytesConfig(
        load_in_8bit = True,
        llm_int8_enable_fp32_cpu_offload = True  # enable CPU offload
    )

# load language model and tokeniser
# 載入語言模型和分詞器
model_name = 'microsoft/Phi-3.5-mini-instruct' # You can replace it with any other model you like
# 可替換成任何喜歡的模型

# set a pretrainmodel as a tokeniser; use_fast = True: Rust implementation for efficiency
# 將預訓練模型設為分詞器；use_fast = True: 使用 Rust 實作以提高效率
tokeniser = AutoTokenizer.from_pretrained(model_name, use_fast = True) # set it to False will lead to python implementation
# 設為 False 會使用 Python 實作

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config = bnb_config if torch.cuda.is_available() else None,
    # load_in_8bit = True,  # use 8-bit quantisation for memory efficiency
    device_map = 'auto' if torch.cuda.is_available() else 'cpu',  # force to use cpu if there isn't CUDA
)

# placeholder for the knowledge base (to be replaced with your actual data)
# 知識庫（內容可替換為實際數據、知識）
knowledge_base = [
    {'text': 'The capital of France is Paris.'},
    {'text': 'The Eiffel Tower is located in Paris.'},
    {'text': 'Python is a popular programming language.'},
    {'text': 'Fortran is regaining its popularity again'},
    {'text': 'Open source is the best idea in software development.'},
    {'text': 'Scihub is a great tool for academic research.'}
]

# create embeddings for the knowledge base
# 為知識庫創建嵌入向量 (embeddings)
embedder = SentenceTransformer('all-mpnet-base-v2')
knowledge_embeddings = embedder.encode([item['text'] for item in knowledge_base])

# build the FAISS index
# 建立 FAISS 索引
index = faiss.IndexFlatL2(knowledge_embeddings.shape[1])
index.add(knowledge_embeddings)

# define a function to retrieve the most similar data from knowledge base
# 定義函數以從知識庫抓出最相似者
def get_relevant_documents(query, top_k = 1): # top_k is the number of relevant documents to retrieve
    # top_k: 要抓出的相關文件數量

    # encode the query into embedding
    # 將查詢編碼為嵌入向量 (embedding)
    query_embedding = embedder.encode(query)

    # Distance and Indices from FAISS
    # 從 FAISS 取得距離 (Distance) 和索引 (Indices)
    D, I = index.search(query_embedding.reshape(1, -1), k = top_k)

    # retrieve the relevant documents
    # 抓出相關文件
    relevant_docs = [knowledge_base[i] for i in I[0]]
    return relevant_docs

# define the chatbot function
# 定義聊天機器人函數
def chat_with_bot(user_input):
    # using RAG to map the question with answer in knowledge base
    # 用 RAG 從知識庫抓出與問題相應的答案
    relevant_docs = get_relevant_documents(user_input)
    context = '\n'.join([doc['text'] for doc in relevant_docs])
    
    # customising your own prompt here
    # 可在此客製化提示詞 (prompt)
    prompt = f'''You are a helpful assistant, and you must answer the question 'BRIEFLY' in the same language with question.
    
    info: {context}

    Question: {user_input}
    '''
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    inputs = tokeniser(prompt, return_tensors='pt').to(device) # force to use cpu if cuda is unavailable
    # 如果沒 cuda，就強制用 cpu 

    # using pytorch for inference without remembering the gradient calculation for memory efficiency
    # 用 pytorch 推論，不記住梯度以節省記憶體
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens = 50) # set the max length of the output # 設定輸出的最大長度
    response = tokeniser.decode(outputs[0], skip_special_tokens = True)

    # Ensure prompt has a newline character
    # Remove the prompt from the response
    # 確保提示詞有換行符號、移除回答中的提示詞 (prompt)
    response = response[len(prompt):].replace('Answer: ', '')

    # Split the response by newline characters
    # 用換行符號分割回答
    parts = response.split('\n', 2)

    # If there are at least two newline characters, remove the content after the second one
    # 如果有兩個換行符號，移除第二個換行符號後的內容
    if len(parts) > 2:
        response = parts[0] + '\n' + parts[1]

    print(response)
    return response.strip()

#======================== cerebrum ========================#



# instantiate the flask app
# 實例化 Flask app
app = Flask(__name__)

# setting up the LINE Bot access token and secret in config.py
# 在 config.py 中設定 LINE Bot 的 access token 和 secret
from config import Config
config = Config()
configuration = Configuration(access_token = config['YOUR_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(config['YOUR_CHANNEL_SECRET'])



# Paste the url generated by tunnelmole (or localtunnel) here
# 將 tunnelmole (或 localtunnel) 生成的網址貼於此
prefix_url = ''



'''
route for the webhook
'''
# configuring the route for the webhook on Line developer console
# 設定 Line developer console 上的 webhook
@app.route('/callback', methods = ['POST'])
def callback():
    # get X-Line-Signature header value
    # 取得 X-Line-Signature 標題值
    signature = request.headers['X-Line-Signature']

    # get request body as text
    # 取得請求主體並轉為文字
    body = request.get_data(as_text = True)
    app.logger.info('Request body: ' + body)

    # handle webhook body
    # 處理 webhook 主體
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info('Invalid signature. Please check your channel access token/channel secret.')
        abort(400)

    return 'OK'

# set a root route just for test
# 設定測試用的根路徑
@app.route('/', methods = ['POST', 'GET'])
def index_page():
    return 'Hello, this is your LINE bot\'s homepage!'

# set a route for file upload
# 設定上傳檔案的路徑
@app.route('/files/<path>')
def get_tmp_path(path):
    return send_from_directory('files', path)

# handling the text message
# 處理文字訊息
@handler.add(MessageEvent, message = TextMessageContent)
def handle_text_message(event):
    print('successfully get into text message handler')
    with ApiClient(configuration) as api_client:
        print('successfully get into api client')
        # instantiate message api object
        # 建立 Messaging API 物件
        api_instance  = MessagingApi(api_client)

        # get reply token
        # 取得 reply token
        replyToken = event.reply_token

        # get message context
        # 取得訊息內容
        replyText = event.message.text

        # prepare the messages for reply (max: 5)
        # 準備要回傳的訊息 (最多五則)
        list_reply = [
            # 測試用訊息
            # TextMessage(text = 'just a test'), # text message for test
            # 回傳使用者的訊息
            # TextMessage(text = replyText), # echo the user's message
            # chatbot 的回答
            TextMessage(text = chat_with_bot(replyText)), # chatbot answer
        ]

        # reply to the user via Line Webhook
        # 透過 Line Webhook 回傳訊息給使用者
        api_instance.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token = replyToken,
                messages = list_reply,
            )
        )

# image message handler
# 圖片訊息處理
@handler.add(MessageEvent, message = ImageMessageContent)
def handle_image_message(event):
    with ApiClient(configuration) as api_client:
        # instantiate message api object
        # 建立 Messaging API 物件
        api_instance  = MessagingApi(api_client)

        # get replyToken
        # 取得 replyToken
        replyToken = event.reply_token
        
        # get message ID
        # 取得 message ID
        messageId = event.message.id

        # set request header
        # 設定請求標題
        my_headers = {
            'Authorization': f'Bearer {config["YOUR_CHANNEL_ACCESS_TOKEN"]}',
        }

        url = f'https://api-data.line.me/v2/bot/message/{messageId}/content'

        # request sending
        # 送出請求
        response = requests.get(url = url, headers = my_headers)

        # save the image (response.content is binary data)
        # 儲存圖片 (response.content 是二進位資料)
        with open(f'files/{messageId}.jpg', 'wb') as file:
            file.write(response.content)

        replyText = f'image received, {messageId}.jpg'

        # prepare the messages for reply (max: 5)
        # 準備要回傳的訊息 (最多五則)
        list_reply = [
            TextMessage(text = replyText),
            ImageMessage(original_content_url = f'{prefix_url}/files/{messageId}.jpg', preview_image_url = f'{prefix_url}/files/{messageId}.jpg')
        ]

        # reply to the user via Line Webhook
        # 經由 Line Webhook 回訊息給使用者
        api_instance.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token = replyToken,
                messages = list_reply
            )
        )

# video message handler
# 影片訊息處理器
@handler.add(MessageEvent, message = VideoMessageContent)
def handle_video_message(event):
    with ApiClient(configuration) as api_client:
        # instantiate the API class
        # 建立 API 實體
        api_instance = MessagingApi(api_client)

        # get the reply token
        # 取得 reply token
        replyToken = event.reply_token
        
        # get message id
        # 取得訊息 id
        messageId = event.message.id

        # set the request header
        # 設定請求標題
        my_headers = {
            'Authorization': f'Bearer {config["YOUR_CHANNEL_ACCESS_TOKEN"]}',
        }

        url = f'https://api-data.line.me/v2/bot/message/{messageId}/content'

        # execute the request
        # 執行請求
        response = requests.get(url = url, headers = my_headers)

        # save the video (response.content is binary data)
        # 儲存影片 (response.content 是二進制資料)
        with open(f'files/{messageId}.mp4', 'wb') as file:
            file.write(response.content)

        replyText = f'video received, {messageId}.mp4'

        # prepare the messages for reply (max: 5)
        # 準備要回傳的訊息 (最多 5 個)
        list_reply = [
            TextMessage(text = replyText),
            VideoMessage(original_content_url = f'{prefix_url}/files/{messageId}.mp4', preview_image_url = f'{prefix_url}/files/{messageId}.mp4')
        ]

        # send the reply messages
        # 回傳訊息
        api_instance.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token = replyToken,
                messages = list_reply
            )
        )

# audio message handler
# 音訊處理
@handler.add(MessageEvent, message = AudioMessageContent)
def handle_audio_message(event):
    with ApiClient(configuration) as api_client:
        # instantiate the API class
        # 實體化 API 類別
        api_instance  = MessagingApi(api_client)

        # get the reply token
        # 取得回傳訊息的 token
        replyToken = event.reply_token
        
        # get message id
        # 取得訊息 id
        messageId = event.message.id

        # set request header
        # 設定請求標題
        my_headers = {
            'Authorization': f'Bearer {config["YOUR_CHANNEL_ACCESS_TOKEN"]}',
        }

        url = f'https://api-data.line.me/v2/bot/message/{messageId}/content'

        # request execution
        # 執行請求
        response = requests.get(url = url, headers = my_headers)

        # save the audio file (response.content is binary data)
        # 儲存音檔 (response.content 是二進制資料)
        with open(f'files/{messageId}.m4a', 'wb') as file:
            file.write(response.content)

        replyText = f'audio received, {messageId}.m4a'

        # replying messages preparation (max: 5)
        # 回應訊息準備 (最多五則)
        list_reply = [
            TextMessage(text = replyText),
            AudioMessage(original_content_url = f'{prefix_url}/files/{messageId}.m4a', duration = 1000)
        ]

        # send the reply messages
        # 發送回覆
        api_instance.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token = replyToken,
                messages = list_reply
            )
        )



#====================================== execution ======================================#



app.run(
    # 開啟除錯模式
    debug = True,     # open debug mode
    # 啟動服務
    host = '0.0.0.0', # serve at 0.0.0.0
    # 設定埠號
    port = 1989       # use port 1989 (or any port you prefer)
)
    
    # if you have your own SSL certs, uncomment the following setting and modify the ssl_context value
    # 若有自己的 SSL 憑證，則可取消下列註解並修改 ssl_context 的值
    # app.run(
    #     debug = True,     # open debug mode
    #     host = '0.0.0.0', # serve at 0.0.0.0
    #     port = 1989,      # use port 1989 (or any port you prefer)
    #     # ssl_context = ('/certs/fullchain4.pem', '/certs/privkey4.pem') # set SSL certification for LINE Bot Webhook
    # )
