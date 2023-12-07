import random 
import time

import csv
import pandas as pd
import numpy as np

#載入已訓練好的模型來做預測
# from joblib import load


#改
ServerURL = 'https://class.iottalk.tw' #For example: 'https://iottalk.tw'

MQTT_broker = None # MQTT Broker address, for example:  'iottalk.tw' or None = no MQTT support
"上面的MQTT Broker 用的話，會把dummy sensor的值 也print出來"
MQTT_port = 5566
MQTT_encryption = True
MQTT_User = 'iottalk'
MQTT_PW = 'iottalk2023'

device_model = 'Dummy_Device'
IDF_list = ['Dummy_Sensor']
ODF_list = ['Dummy_Control']
# 期中project 要改MAC address
device_id = None #if None, device_id = MAC address  #我試過，如果改了好像print不出來
# 可以改device name
device_name = 'jiang_1121'
# 我設每0.1秒讀取一次
exec_interval = 0.1  # IDF/ODF interval

def on_register(r):
    print('Server: {}\nDevice name: {}\nRegister successfully.'.format(r['server'], r['d_name']))

"""for inference"""
#載入模型 舊版
# from joblib import load
# decisionTreeModel=load('decision_tree_model')
# print(decisionTreeModel)
import pickle
decisionTreeModel = 'decision_tree_model.pkl'
with open(decisionTreeModel,'rb')as file: 
    md=pickle.load(file)
file.close()


#模型function  
def ml_predict(inputData):
    
    result=md.predict(inputData)
    # print("result",result)  #1,2,3
    return result

#一個動作需要一秒鐘，因為每0.1秒就會收集一次資料所以會收集10次，共60筆 
count=1
oneData=[]
datalist=[]

light=50
"""for inference"""

"""for 上課作業"""
# 使用 dummy device 作為 input
# light=0
# flip=0
order=0
"""for 上課作業"""
def Dummy_Sensor():
    """for 上課作業"""
    # """暗變亮，量變暗"""
    # global light
    # global flip
    # if flip==0:
    #     light=light+10
    #     if light==100:
    #         flip=1
    # else:
    #     light=light-10
    #     if light==0:
    #         flip=0
    # return light
    # """紅綠燈"""
    # r=255,0,0
    # g=0,255,0
    # y=255,255,0
    # global order
    # order=order+1
    # if order%3==1:
    #     return r
    # elif order%3==2:
    #     return y
    # else:
    #     return g
    """for 上課作業"""
    
    # """原本範例"""
    # return random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100) 

    """for inference"""
    return light
    """for inference"""

"""for 收集資料"""
count_for_dictwriter=1
"""for 收集資料"""
# 當作output
def Dummy_Control(data:list):
    """原本範例"""
    # print(data[0])    #[]
    # print(data)   #[[]]

    """for 收集資料 begin"""

    # """
    # 將sensor寫檔
    # 寫檔用任何一種方法均可
    # """

    # "使用DictWriter   ,import csv"
    # # circle.csv  line.csv  other.csv
    # with open('other.csv','a',newline='') as file:
    #     # 將dictionary 寫入 csv檔
    #     writer=csv.DictWriter(file,['acc1','acc2','acc3','pyro1','pyro2','pyro3'])
    #     # 寫入第一列的欄位名稱
    #     # writer.writeheader()

    #     global count_for_dictwriter
    #     print("-----  count  =  ",count_for_dictwriter)
    #     print(data[0][0],data[0][1],data[0][2],data[0][3],data[0][4],data[0][5])
    #     if(count_for_dictwriter%10==0):
    #         print("收集完第",count_for_dictwriter//10,"組資料(每一組資料含10筆，一筆有6個數值)")
    #     else:
    #         print("收集",count_for_dictwriter%10,"/10 ......")
        
    #     writer.writerow({'acc1':data[0][0],'acc2':data[0][1],'acc3':data[0][2],'pyro1':data[0][3],'pyro2':data[0][4],'pyro3':data[0][5]})

    #     count_for_dictwriter=count_for_dictwriter+1
    #     print("==========")

    """for 收集資料 end"""


    """for inference begin"""
    global count
    global oneData
    global datalist
    global light

    if count % 10 != 0 and count !=0:
        print("正在收集",count,"/10資料")
        oneData=[data[0][0],data[0][1],data[0][2],data[0][3],data[0][4],data[0][5]]
        datalist.append(oneData)
        count+=1
    else:
        oneData=[data[0][0],data[0][1],data[0][2],data[0][3],data[0][4],data[0][5]]
        datalist.append(oneData)
        print("收集完一單位資料(60個數值)--------------------")
        #print(datalist)
        count=1
        oneData=[]
        
        #一定要加這一行 reshape把資料變成一格陣列
        datalist=pd.DataFrame(np.array(datalist).reshape(1,-1),columns=['acc1_1','acc2_1','acc3_1','gyro1_1','gyro2_1','gyro3_1','acc1_2','acc2_2','acc3_2','gyro1_2','gyro2_2','gyro3_2','acc1_3','acc2_3','acc3_3','gyro1_3','gyro2_3','gyro3_3','acc1_4','acc2_4','acc3_4','gyro1_4','gyro2_4','gyro3_4','acc1_5','acc2_5','acc3_5','gyro1_5','gyro2_5','gyro3_5','acc1_6','acc2_6','acc3_6','gyro1_6','gyro2_6','gyro3_6','acc1_7','acc2_7','acc3_7','gyro1_7','gyro2_7','gyro3_7','acc1_8','acc2_8','acc3_8','gyro1_8','gyro2_8','gyro3_8','acc1_9','acc2_9','acc3_9','gyro1_9','gyro2_9','gyro3_9','acc1_10','acc2_10','acc3_10','gyro1_10','gyro2_10','gyro3_10'])
        #用模型判斷 #可能這裡的datalist要在處理一下轉成model可以訓練一筆的格式
        predictResult=ml_predict(datalist)  
        #print(predictResult)
        print("-----手勢偵測結果-----")
        if predictResult==1:
            print("偵測到畫圈，燈泡亮度變最亮\n")
            light=100
        elif predictResult==2:    
            print("偵測到往上再往下，燈泡亮度變最暗\n")
            light=1
        else:
            print("沒有偵測到手勢，燈泡亮度變回中間值\n")
            light=50

        datalist=[]
        # print("現在亮度為=",light)
        print("=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*")

    """for inference end"""
    


