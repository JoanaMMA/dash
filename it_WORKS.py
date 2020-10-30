# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 11:43:38 2020

@author: xXJaneXx
"""



from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np

from sklearn import metrics
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

import pickle
import joblib
from joblib import dump, load 
import category_encoders as ce
from sklearn.pipeline import make_pipeline

from pprint import pprint

# Get the data and change ? to nan-values
cle = pd.read_csv('processed.cleveland.csv', keep_default_na=False, na_values=["?"])

# Change num to goal
cle.rename(columns={'num': 'goal'}, inplace=True) 

# Replacing NaN-values with most frequent

replc = SimpleImputer(strategy= 'most_frequent')
replc = replc.fit_transform(cle)
cle = pd.DataFrame(replc, columns=cle.columns)

#Labels
# Everything except goal x axis
cle_features = cle.drop(['goal'], axis=1)
# Only goal y axis
cle_label = cle['goal'] 

#normalization
feat_NoNorm = cle_features.drop(['age', 'trestbps', 'chol', 'oldpeak', 'thalach'], axis=1)
numerical = 'age', 'trestbps', 'chol', 'thalach', 'oldpeak', 
X = cle_features[[c for c in cle_features if c in numerical]]

scaler = StandardScaler()
feat_norm = scaler.fit_transform(X)
feat_norm = pd.DataFrame(feat_norm, columns=X.columns)

cle_feat = pd.concat([feat_norm,feat_NoNorm], axis=1)

# print(cle_features.head())

#train
X_train, X_test, y_train, y_test = train_test_split(cle_features, cle_label, test_size=0.3, random_state=321, stratify=cle_label)

lrclf_best = LogisticRegression(multi_class='ovr', penalty='l2', C=464.15888336127773, solver='lbfgs', max_iter=2000)
lrclf_best.fit(X_train, y_train)

model=lrclf_best

y_pred_lr = lrclf_best.predict(X_test)


confusion_matrix(y_test, y_pred_lr)


#pipeline
steps = [('scaler',StandardScaler()),('cle_feat',ce.OrdinalEncoder(cle_feat)),('lrclf_best',LogisticRegression())]
hd_model = make_pipeline (StandardScaler(),ce.OrdinalEncoder(cle_feat), model)



