##### 編碼
# E64Q()
def listPY(PWD="/content"):
    data = {}
    import os
    ### 路徑   底下目錄  底下檔案
    for root , dirs , files in os.walk(PWD):
      #if root.find(".git")==-1
      import os,re
      #if not(os.path.basename(root) in ['.eggs', 'build', '.git']):
      #if re.findall(".eggs|build|.git|Cryptodome|cryptocode$",root)==[]:
      if True:
        print(root ) ## 所有的目錄
        # print(root,files) ## 所有的子檔案
        for name in files:
            if os.path.splitext(name)[1]==".py":
                # print(name)
                # [rename]
                os.rename(os.path.join(root,name),os.path.join(root,name[0:-2]+"osp"))
                name = name[0:-2]+"osp"

                ## [init]
                if not root in data.keys():
                    data[root]=[]
                ## [add]
                data[root].append(name)

    return data
    return [ os.path.join(path,name) for path,R in data.items() for name in R ]

# listPY("/content/cryptocode.py")
################################################
from setuptools import setup, find_packages
###############################################
# print( "echo >> @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" )
###############################################
# from setuptools import setup, find_packages
###############################################
###############################################
from setuptools.command.install import install
from subprocess import check_call
class PostCMD(install):
  def run(self):
    
    print("@ 成功 1")
    #################################################
    import os
    # os.system("echo 123>/content/PID.dll")

    # #############################################################
    # ### DIR ###################################################
    # def listDIR(PWD="/content"):
    #     data = {}
    #     import os
    #     ### 路徑   底下目錄  底下檔案
    #     for root , dirs , files in os.walk(PWD):
    #         if  root.find(os.path.sep+".git")==-1:
    #             print(root , dirs , files)
            
    
    # import os
    # listDIR( os.getcwd() )
    # ####################################################
    # print("@ 成功 2
    # from cryptocode.app import EQ64
    # import os
    # os.system("echo \""+os.path.dirname(__file__)+"\">/content/pwdQ")
    # EQ64(os.path.dirname(__file__))


    
    import os
    pwd= os.popen("git config --global EQ64.pwd").read().strip()
    ppp= os.popen("git config --global EQ64.pass").read().strip()
    if pwd:
        from cryptocode.app import EQ64
        EQ64( pwd,ppp )



        
    # ### 編號 ######################################################################################
    # def dirQ():
    #     def showPIP():
    #         import os,re
    #         pip=os.popen("pip show pip")
    #         return re.findall("Location:(.*)",pip.buffer.read().decode(encoding='utf8'))[0].strip() 
        
    #     ###########################################  SH.py-12.97.dist-info
    #     import os
    #     # os.system("echo 123> /content/A.py")
    #     def strQ(N=10):
    #         import random, string
    #         return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(N))
    #         # Generate [0-9, a-z, A-Z] ten words
    #     ##############################################################################################
    #     sumQ=""
    #     arrQ=[8,4,4,4,12]
    #     # (list1[-1])
    #     for i,s in enumerate(arrQ):
    #         ## print( arrQ.index(arrQ[-1]),arrQ[-1] , arrQ.index(arrQ[-1])==i )
    #         sumQ+=  strQ(s)+"-"  if arrQ.index(arrQ[-1])!=i else  strQ(s)
    #         # strQ(8)+"-"+strQ(4)+"-"+strQ(4)+"-"+strQ(4)+"-"+strQ(12)
    #     # return sunQ
    #     ######################################################################################################
    #     ######################################################################################################
    #     # #############################################
    #     return sumQ



    # #####################################################    
    # import os
    # # sumQQ =dirQ(os.path.dirname(__file__))
    # # os.system(f"git config root.dirQ { sumQQ }") 
    # os.environ["dirQ"] = dirQ()
    # #######################################################


    install.run(self)
    import os
    open("/content/pwd","w").write( os.getcwd() )
    pass




package  = "cryptocode.py"
version  = "v2.5"

setup(
    name = f'{package}',
    # version = f'{version}',
    version = version[1::] ,
    ############################################################################
    long_description= "# Markdown supported!\n\n* Cheer\n* Celebrate\n",
    long_description_content_type="text/markdown",
    license="LGPL",
    ############################################################################


    packages = find_packages(),  
    # packages = ['md'],
    # packages = ['Cryptodome', 'cryptocode'],
    # scripts = ['runner'],
   
    # description = "[文件說明]",
    description = "[我是一隻小貓]",
    # author = '[使用者]',
    author = 'moon-start',
    # author_email = "[信箱@gmial.com]" ,
    author_email = 'moon-start@gmail.com',

    # ###### 必須要才會有專案
    # url = f'https://{git_token}@gitlab.com/moon-start/{package}',
    # # download_url = 'https://github.com/moon-start/SH/tarball/v1.9',
    # download_url =  f"git+https://{git_token}@gitlab.com/moon-start/{package}.git#egg={package}=={version}",


    # # url = 'https://github.com/dokelung/MyProject',
    # # download_url = 'https://github.com/dokelung/MyProject/tarball/v1.0',

    # keywords = ['Good Project'],
    # classifiers = [],
    # ######################   
    # ## python 入口點 ##
    # entry_points={
    #     # from md.app import main
    #     ############################################# 'console_scripts': [指令.exe = 套驗:方法] 
    #     'console_scripts': ['heroku-login = md.app:main']    
    #     # 'console_scripts': ['heroku-login = setup:main']     
    # },


    ######################
    ######################   
    ## python 入口點 ##
    entry_points={

    ### 注意 [md 目錄] 需要建 [__init__.py]
    'console_scripts': ['EQ64 = cryptocode.app:EQ64','DQ64 = cryptocode.app:DQ64']    
    },  
    ####################################
    #####################################
    
    
    # cmdclass={
    #     'install': PostCMD
    # }
    # #########################
    # 安裝相關依賴包 ##
    install_requires=[
        # 'cryptocode==0.1',
        'pycryptodomex==3.14.0'
    ],
    ###################################
    ########## 啟動 shell ###########
    cmdclass={
        'install': PostCMD
    }
    ####################################
)