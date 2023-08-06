
################################################
class initQ:
  def __new__(cls): # 不備呼叫
    import os
    # print(os.path.dirname(__file__) )
    #############################
    ### 只顯示 目錄路徑 ----建立__init__.py
    for dirPath, dirNames, fileNames in os.walk(os.path.dirname(__file__)):
        ##########################################################################
        import re
        if re.findall(".*"+os.path.sep+".git.*",dirPath)==[]:    
            # print(re.findall(".*"+os.path.sep+".git.*",dirPath)  )
            # print( dirPath )
            print( "echo >> "+dirPath+f"{ os.sep }__init__.py" )
            os.system("echo >> "+dirPath+f"{ os.sep }__init__.py") 
        ########################################################################## 
print( "echo >> @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" )
# Running command python setup.py egg_info
import sys
if "egg_info" in sys.argv:
    initQ()
print( "echo >> @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" )


###############################
import sys,os
from cryptocode.app import EQ64
################################
home=os.path.dirname(__file__)
os.chdir("."+os.path.sep+"build"+os.path.sep+"lib")
EQ64()
os.chdir(home)
################################