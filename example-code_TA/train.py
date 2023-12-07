from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd

# 讀入檔案
data=pd.read_csv("combine.csv")

# X=data.drop('label',axis='columns') 
# y=data['label'] 
inputs=data.drop('label',axis='columns') #inputs放需要訓練的欄位
target=data['label'] #target放label
# print(target.head())

#拆分訓練集與測試集
# X=inputs
# y=target
# X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
# model=DecisionTreeClassifier().fit(X_train,y_train)
# 用建立好的模型來預測資料
# model.predict(X_test)
# 檢驗模型的正確率
# model.score(X_test,y_test)

#沒拆
X=inputs
y=target


"使用自己選擇的模型"
model=DecisionTreeClassifier().fit(X,y)

"通常會用測試集看分數，因為我沒有額外紀錄其他sensor data"
# print("model score=",model.score(X,y))

#匯出模型
# from joblib import dump #需要使用舊版本的python1.10.0 和 scikit-learn=1.1.3
# dump(model,'decision_tree_model')

import pickle

model_filename='decision_tree_model.pkl'
with open(model_filename,'wb')as file: 
    pickle.dump(model,file)

print("模型已訓練完畢")