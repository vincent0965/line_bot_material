LINE Bot
可在LINE上面進行對話與互動


設定local link -> Ngrok連線指令
Ngrok.exe http 5000 -region ap
生成網址後連接line的api

檔案封裝上雲端:

上傳 heroku:

    上傳
    app.run(host='0.0.0.0',port=os.environ['PORT'])
    
    連接測試
    app.run()
    

