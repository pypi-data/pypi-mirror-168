
### 加密 #####################
# def EQ64(pathQ="/content/R.py"):
def EQ64(pathQ=None,wow="520"):
  import os,sys
  if   len(sys.argv)==1:
      print("@ 請輸入一個 加密參數 .")
  else:
    # wow = sys.argv[1]
    # pathQ = os.getcwd()
    
    import os
    #############################
    if pathQ==None:
        import sys
        pathQ = sys.argv[1]
    ##############################
    if  pathQ.endswith("setup.py"):
        pathQ =os.path.dirname(pathQ)  
   

    def E64Q(path="/content/R.py"):
        import base64
        image = open( path , 'rb')
        valueQ = base64.b64encode(image.read()).decode()
        ###########################################
        import os
        import cryptocode
        #################################################
        # os.system("git init ") ## 在當前 建立專案key
        # wow = os.popen("git config root.dir").read().rstrip()
        # wow = "123"
        value = cryptocode.encrypt(valueQ, wow )
        # print(value)
        open( path , 'w').write(value)


    ##### 編碼
    # E64Q()
    def listPY(PWD="/content"):
        data = {}
        import os
        ### 路徑   底下目錄  底下檔案
        for root , dirs , files in os.walk(PWD):
            # print(root) ## 所有的目錄
            # print(root,files) ## 所有的子檔案
          if os.path.basename(root) in [i for i in os.listdir( PWD )if i[0]!="."] :
            for name in files:
                if os.path.splitext(name)[1]==".py":
                    print("加密了!!",root ,name )
                    # print(name)
                    ## [rename]
                    os.rename(os.path.join(root,name),os.path.join(root,name[0:-2]+"osp"))
                    name = name[0:-2]+"osp"

                    ## [init]
                    if not root in data.keys():
                        data[root]=[]
                    ## [add]
                    data[root].append(name)

        # return data
        return [ os.path.join(path,name) for path,R in data.items() for name in R ]
        


    # import os
    if pathQ!=None:
        for i in listPY(pathQ):
            E64Q(i)



### 解密 #####################
# def DQ64(pathQ="/content/R.py"):
def DQ64(pathQ=None,wow="520"):
  import os,sys
  if   len(sys.argv)==1:
      print("@ 請輸入一個 加密參數 .")
  else:
    # wow = sys.argv[1]
    # pathQ = os.getcwd()
    
    import os
    #############################
    if pathQ==None:
        import sys
        pathQ = sys.argv[1]
    ##############################
    if  pathQ.endswith("setup.py"):
        pathQ =os.path.dirname(pathQ) 

    def D64Q(path="/content/R.py"):
        import base64
        image = open( path , 'r',encoding="utf-8").read()
        ###########################################
        import os
        # os.system("pip install cryptocode > log.py") 
        import cryptocode
        # os.remove("log.py")
        ############################################
        # wow = os.popen("git config root.dir").read().rstrip()    
        # os.system(f'start cmd /c "timeout /nobreak /t 3&& echo { str(wow) }222@@ && pause"')

        # wow = os.environ[ "Email" ].split("@")[0][::-1]

        # 使用 try，測試內容是否正確
        BL=True # 放在外面 if同一層
        try:             
            valueQ = cryptocode.decrypt(image, wow )
            # print(value)
            value = base64.b64decode(valueQ).decode('utf-8') ## 解碼 2進位為中文碼
            # print('發生錯誤!')
        except:                   
        # 如果 try 的內容發生錯誤，就執行 except 裡的內容
            BL=False
            # print('錯誤處理')

        if BL:
            # print("@ w ")
            ############################################
            # value = base64.b64decode(image).decode('utf-8') ## 解碼 2進位為中文碼
            # print(value.decode('utf-8'),type(value))
            # print(value)

            
            ## [rename] ###########################
            os.rename( path , path[0:-3]+"py")
            path = path[0:-3]+"py"
            ########################################

            open( path , 'w').write(value)


    ##### 解碼
    # D64Q()


    def listPY(PWD="/content"):
        data = {}
        import os
        ### 路徑   底下目錄  底下檔案
        for root , dirs , files in os.walk(PWD):
            # print(root) ## 所有的目錄
            # print(root,files) ## 所有的子檔案

            for name in files:
                if os.path.splitext(name)[1]==".osp":
                    # print(name)
                    
                    ## [rename]
                    os.rename(os.path.join(root,name),os.path.join(root,name[0:-3]+"py"))
                    name = name[0:-3]+".py"

                    ## [init]
                    if not root in data.keys():
                        data[root]=[]
                    ## [add]
                    data[root].append(name)

        # return data
        return [ os.path.join(path,name) for path,R in data.items() for name in R ]
        

    # print("@",listPY( pathQ ))
    # import os
    if pathQ!=None:
        for i in listPY( pathQ ):
            # print(i)
            D64Q(i)

