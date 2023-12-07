"""
先把10筆(1筆包含6個數值)資料串成一列

combine.csv
每一列60個數值，共300列(circle.csv,line.csv,other.csv各100列)
最後加上label(circle:1,line:2,other:3)

用法:
"""

import csv

rowInTen=[]#存一列60個數值
datas=[]#存100列rowInTen
count=0
# circle.csv,line.csv,other.csv
with open('other.csv') as file:
    data=csv.reader(file)#使用csv.reader讀出來的的資料是list
    for row in data:
        #每10筆換一行
        if count%10==0 and count!=0:    
            datas.append(rowInTen)   #append:向列表尾部添加新元素 ，但這裡是把list串到list中  先把之前rowInTen的資料append到datas  append用法前面不須賦值
            rowInTen=[] #再把rowInTen清空
            rowInTen=rowInTen+row        
            count+=1
        else:
            rowInTen=rowInTen+row   #這樣寫是list串接
            count+=1

#print(type(datas))#list
print(len(datas))
#寫檔combine.csv
for i in datas:
    #開啟輸出的 CSV 檔案
    with open('combine.csv','a',newline='') as csvfile:
        #建立 CSV 檔寫入器
        writer=csv.writer(csvfile)
        #寫入一列資料
        writer.writerow(i)