import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
import joblib
import os

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
#load data
print("loading data..")
#df = pd.read_csv(os.path.join(basedir, "../data/bank.csv"), header = None, names=['age','job','marital','education','default','balance','housing',
#                                                            'loan','contact','day_of_week','month','duration','campaign','pdays',
#                                                            'y'])
df = pd.read_csv(os.path.join(basedir, "../data/bank.csv"))
print("data preprocessing..")
#drop campaign related columns
df.drop(df.iloc[:, 8:16], inplace = True, axis = 1)
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

['age','job','marital','education','default','housing','loan','balance','contact','day_of_week','month','duration','campaign','pdays','y']

#extract numeric features 
numeric_data = df.iloc[:, [0, 5]].values
numeric_df = pd.DataFrame(numeric_data, dtype = object)
numeric_df.columns = ['age', 'balance']

#standard scaling age
age_std_scale = StandardScaler()
numeric_df['age'] = age_std_scale.fit_transform(numeric_df[['age']])
#standard scaling balance
balance_std_scale = StandardScaler()
numeric_df['balance'] = balance_std_scale.fit_transform(numeric_df[['balance']])

#extract categoric features
X_categoric = df.iloc[:, [1,2,3,4,6,7]].values

#onehotencoding
ohe = OneHotEncoder()
categoric_data = ohe.fit_transform(X_categoric).toarray()
categoric_df = pd.DataFrame(categoric_data)
categoric_df.columns = ohe.get_feature_names()

#combine numeric and categorix
X_final = pd.concat([numeric_df, categoric_df], axis = 1)

x_train,x_val,y_train,y_val=train_test_split(X_final,y,train_size=0.8,random_state=42)
print("model training")
#train model
rfc = RandomForestClassifier(n_estimators = 100)
rfc.fit(x_train, y_train)
y_pred = rfc.predict(x_val)
print(confusion_matrix(y_val,y_pred))
print(accuracy_score(y_val,y_pred))
print("model saving")
filename = os.path.join(basedir, '../models/finalized_model.pickle')
joblib.dump(rfc, filename)
print("All done")