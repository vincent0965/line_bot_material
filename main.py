# 啟用伺服器基本樣板
# 引用套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import json

import os
# 伺服器準備 連接到LINE的API
app = Flask(__name__)

line_bot_api = LineBotApi('LINE_API')
handler = WebhookHandler('WEBHANDER')

# 啟用server對外接口 可以讓lin的消息送進來
@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# ==============================================================

# 將消息模型，文字收取消息與文字寄發消息 引入
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, ImageSendMessage)

# 設定加入好友回復清單
reply_message_list = [
    TextSendMessage(text="研究生不死，只是生不如死。"),
    TextSendMessage(text="請選擇今天的行程~")
]

# 載入Follow事件
from linebot.models.events import (FollowEvent)

# 載入requests套件
import requests

# handler.add 意思為 如果收到xxEvent 就執行下列的作法
# 告知handler，如果收到FollowEvent，則做下面的方法處理
@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event):
    # 請 line_bot_api 回覆消息給用戶
    # reply_messange(event.reply_token, [寄給用戶的消息 最多五則])
    line_bot_api.reply_message(event.reply_token, reply_message_list)

'''
handler處理文字消息

收到用戶回應的文字消息，
按文字消息內容，往素材資料夾中，找尋以該內容命名的資料夾，讀取裡面的reply.json

轉譯json後，將消息回傳給用戶
'''

# 引用套件
from linebot.models import (
    MessageEvent, TextMessage
)

'''
消息判斷器

讀取指定的json檔案後，把json解析成不同格式的SendMessage
讀取檔案 把內容轉換成json
將json轉換成消息 放回array中，並把array傳出。
'''
# 引用會用到的套件
import json
from linebot.models import (
    ImagemapSendMessage, TextSendMessage, ImageSendMessage, LocationSendMessage, FlexSendMessage, VideoSendMessage, StickerSendMessage, AudioSendMessage
)

from linebot.models.template import (
    ButtonsTemplate, CarouselTemplate, ConfirmTemplate, ImageCarouselTemplate

)

from linebot.models.template import *

def detect_json_array_to_new_message_array(fileName):
    # 開啟檔案，轉成json 程式碼編碼需要注意(utf8)
    # 因 window的預設編碼是 cp980 要將編碼調整為 utf8

    with open(fileName, encoding='utf8') as f:
        jsonArray = json.load(f)

    # 解析json
    returnArray = []
    for jsonObject in jsonArray:

        # 讀取其用來判斷的元件
        message_type = jsonObject.get('type')

        # 轉換
        if message_type == 'text':
            returnArray.append(TextSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'imagemap':
            returnArray.append(ImagemapSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'template':
            returnArray.append(TemplateSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'image':
            returnArray.append(ImageSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'sticker':
            returnArray.append(StickerSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'audio':
            returnArray.append(AudioSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'location':
            returnArray.append(LocationSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'flex':
            returnArray.append(FlexSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'video':
            returnArray.append(VideoSendMessage.new_from_json_dict(jsonObject))

            # 回傳
    return returnArray

# '''
# 網頁爬蟲
# '''
# import codecs
# import requests
# import json
# import os
#
# def paper_search(event):
#
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage("請輸入想搜尋的文章名稱:")
#     )
#
#     custom = input(TextMessage)
#
#     r1 = requests.get(
#         # 搜尋網址
#         "https://scholar.google.com.tw/",
#         # 傳遞字元到網頁
#         params = {
#         "q":'%s'%(custom),
#         "page":"1",
#         "sort":"sale/dc"
#         }
#     )
#
#     os.system("cls")
#     r1.encoding = "utf8"
#     ret = r1.json()
#
#     while True:
#         # 載入其他頁面的資料
#         p = input("頁碼：")
#         r2 = requests.get(
#             "https://ecshweb.pchome.com.tw/search/v3.3/all/results",
#             params={
#                 "q":"%s"%(custom),
#                 "page":"%s"%(p),
#                 "sort":"sale/dc"
#             }
#         )



# 文字消息處理
@handler.add(MessageEvent,message=TextMessage)
def process_text_message(event):

    # 判斷檔案路徑是否為json或者txt
    JSON = os.path.exists("material/"+event.message.text+"/reply.json")
    TXT = os.path.exists("material/"+event.message.text+"/reply.txt")

    if JSON == True:
        # 讀取本地檔案，並轉譯成消息
        result_message_array =[]
        replyJsonPath = "material/"+event.message.text+"/reply.json"
        result_message_array = detect_json_array_to_new_message_array(replyJsonPath)

        # 發送
        line_bot_api.reply_message(
        event.reply_token,
        result_message_array
        )

    elif TXT == True:

        # paper_search()

        # 讀取txt檔案
        f = open("material/"+event.message.text+"/reply.txt")
        paper = f.read()

        # 發送訊息
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(paper)
        )


'''
當收到PostBackEvent時(再次地回傳訊息)
告知handler
data為data1 傳文字訊息"a"
data為data2 傳文字訊息"b"
'''
from linebot.models import PostbackEvent
from linebot.models import (
    QuickReply,
    QuickReplyButton,
    MessageAction
)
# 集體烙幹
@handler.add(PostbackEvent)
def handle_postback_event(event):
    postback_data = event.postback.data

    '''
    製作快速按鍵回復
    先做按鍵
    再做QuickReply
    觸發條件(夾帶在SendMessage裡一起送出去)
    '''
    # 創建按鍵
    qrb1 = QuickReplyButton(action = MessageAction(label = "卑鄙源之助", text = "卑鄙源之助"))
    qrb2 = QuickReplyButton(action = MessageAction(label = "人民的法槌", text = "人民的法槌"))
    qrb3 = QuickReplyButton(action = MessageAction(label = "浪漫duke", text = "浪漫duke"))
    # 將按鍵內容封裝起來
    quick_reply_list = QuickReply([qrb1, qrb2, qrb3])

    if postback_data == "data1":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("你的對手在這裡~", quick_reply = quick_reply_list)
        )
    elif postback_data == "data2":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("教授在你背後，他很火")
        )
    elif postback_data == "fit1":

        import random
        # 產生陣列 表示輸贏
        gameList = ("剪刀", "石頭", "布")
        # 從 gameList 中隨機排選一個
        gameChoice = random.choice(gameList)

        while True:

            if (gameChoice == "剪刀"):  # 判斷輸贏
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage("I choose: 剪刀" + ", You choose: "+ "剪刀" +
                                    " ,平手")
                )
            elif (gameChoice == "石頭"):
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage("I choose: 石頭" + ", You choose: "+ "剪刀" +
                                    " ,你輸了")
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage("I choose: 布" + ", You choose: "+ "剪刀" +
                                    " ,你贏了")
                )
    elif postback_data == "fit2":

                import random
                # 產生陣列 表示輸贏
                gameList = ("剪刀", "石頭", "布")
                # 從 gameList 中隨機排選一個
                gameChoice = random.choice(gameList)

                while True:

                    if (gameChoice == "剪刀"):  # 判斷輸贏
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage("I choose: 剪刀" + ", You choose: " + "石頭" +
                                            " ,你贏了")
                        )
                    elif (gameChoice == "石頭"):
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage("I choose: 石頭" + ", You choose: " + "石頭" +
                                            " ,平手")
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage("I choose: 布" + ", You choose: " + "石頭" +
                                            " ,你輸了")
                        )
    elif postback_data == "fit3":

                import random
                # 產生陣列 表示輸贏
                gameList = ("剪刀", "石頭", "布")

                # 從 gameList 中隨機排選一個
                gameChoice = random.choice(gameList)

                while True:

                    if (gameChoice == "剪刀"):  # 判斷輸贏
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage("I choose: 剪刀" + ", You choose: " + "布" +
                                            " ,你輸了")
                        )
                    elif (gameChoice == "石頭"):
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage("I choose: 石頭" + ", You choose: " + "布" +
                                            " ,你贏了")
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage("I choose: 布" + ", You choose: " + "布" +
                                            " ,平手")
                        )

                # ==============================================================

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
    # app.run()
