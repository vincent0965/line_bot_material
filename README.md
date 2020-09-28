開啟Ngrok連線指令
Ngrok.exe http 5000 -region ap
生成網址後連接line的api

檔案封裝上雲端

因為要上傳給 heroku 因此要修改
import os
if __name__ == "__main__":

    上傳
    app.run(host='0.0.0.0',port=os.environ['PORT'])
    
    連接測試
    app.run()
    
只要有更新
1. git add .
2. git commit -am "make it better"
3. git push heroku master