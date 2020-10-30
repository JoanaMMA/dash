# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 15:41:38 2020

@author: xXJaneXx
"""

# import os
import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# import pickle
# import joblib
# from joblib import dump, load 
# import category_encoders as ce
# from sklearn.pipeline import make_pipeline
from it_WORKS import model

screen ={'maxWidth': '960px', 'margin': 'auto'}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server
app.layout = html.Div([
   html.Div([html.H2('Safve Heart',
                      style={'marginLeft': 20, 'color': 'white'}
                     ),
              html.H3('A Predictive Clinical Support System for Heart Disease',
                      style={'marginLeft': 25, 'color': 'white'})
             ],
             style={'border': 'thin black solid',
                    'backgroundColor': '#d61519',
                    'padding': '10px 5px'}),
   html.Div([html.H4( 'Patient data',
                     style={'marginLeft': 25, 'color': 'white'}
                     ),
             html.H5('Use the controls below to update your predicted risk for Heart Disease',
                     style={'marginLeft': 25, 'color': 'white'})
             ],
            style={'border': 'thin black solid',
                    'backgroundColor': 'blue',
                    'padding': '10px 5px'}),

    html.Div([
    dbc.Row([html.Div("Patient information",
                          style={'font-weight': 'bold', 'font-size': 20}),
            html.Div([dcc.Markdown("This patient has a predicted risk of:",
                     style={'font-weight': 'bold', 'font-size': 20}), 
            html.Div(id='patient_data',style={'marginleft': 30,
                               'font-weight': 'bold',
                               'font-color': 'red',
                               'font-weight': 'bold',
                               'font-size': 40,
                               'textAlign': 'center'})])]),
        dbc.Row([html.Div("Demographics", style={
                               'font-weight': 'bold',
                               'font-color': 'black',
                               'font-weight': 'bold',
                               'font-size': 20,
                               'textAlign': 'center'})]),
           dbc.Row([dbc.Col(html.Div([
                   html.Label(children='Age(years): '),
                   dcc.Input(
                       type="number",
                       debounce=True,
                       value= 55.0,
                       id='age')]),
                    width={"size": 3}),   
               dbc.Col(html.Div([
                   html.Label(children='Sex:'),
                   dcc.Dropdown(
                       options=[
                           {'label': 'Female', 'value': 0.0},
                           {'label': 'Male', 'value': 1.0}
                       ],
                       value= 1,
                       id='sex'
                   )]),
                   width={"size": 3})],style={'padding': '10px 10px', 
                                               'Align': 'center'}),
   
       dbc.Row([html.Div("Clinical Findings",
                         style={'marginleft': 30,
                               'font-weight': 'bold',
                               'font-color': 'black',
                               'font-weight': 'bold',
                               'font-size': 20,
                               'textAlign': 'center'})]),

               dbc.Row([dbc.Col(html.Div([
                       html.Label(children='Chest Pain: '),
                       dcc.Dropdown(
                           options=[
                               {'label': 'Asymptomatic', 'value': 4.0 },
                               {'label': 'Typical Angina', 'value': 1.0},
                               {'label': 'Atypical Angina', 'value': 2.0},
                               {'label': 'Non-anginal', 'value': 3.0},
                           ],
                           value= 2.0,
                           id='cp'
                       )]), 
                       width={"size": 3})],style={'padding': '10px 10px', 
                                               'Align': 'center'}),
                dbc.Row([dbc.Col(html.Div([
                       html.Label(children='Systolic Blood Pressure (mmHg): '),
                       dcc.Input(
                           id='trestbps',
                           type="number",
                           debounce=True,
                           value= 140
                       )]), 
                       width='auto')],style={'padding': '10px 10px', 
                                               'Align': 'center'}),
             dbc.Row([dbc.Col(html.Div([
                       html.Label(children='Serum Cholesterol(mg/L): '),
                       dcc.Input(
                           id='chol',
                           type="number",
                           debounce=True,
                           value= 275
                       )]),
                       width='auto')],style={'padding': '10px 10px', 
                                               'Align': 'center'}),                              
            dbc.Row([dbc.Col(html.Div([
                       html.Label(children='Fasting blood sugar >120mg/dl:'),
                       dcc.Dropdown(
                           options=[
                               {'label': 'No', 'value': 0.0},
                               {'label': 'Yes', 'value': 1.0}
                           ],
                           value= 1,
                           id='fbs'
                       )]), 
                       width='auto')],style={'padding': '10px 10px', 
                                               'Align': 'center'}),
             dbc.Row([dbc.Col(html.Div([
                       html.Label(children='Resting ECG:'),
                       dcc.Dropdown(
                           options=[
                               {'label': 'Normal', 'value': 0.0},
                               {'label': 'ST alterations', 'value': 1.0},
                               {'label': 'LVH', 'value': 2.0}
                       ],
                       value= 0,
                       id='restecg'
                       )]),
                       width={"size": 3})],style={'padding': '10px 10px'}),                                
            dbc.Row([dbc.Col(html.Div([
                       html.Label(children='Max Heart Rate (bpm): '),
                       dcc.Input(
                           id='thalach',
                           type="number",
                           debounce=True,
                           value= 100
                       )]), 
                       width='auto')],style={'padding': '10px 10px'}),
                 
    dbc.Row([html.Div("Stress test results",
                     style={
                            'font-weight': 'bold',
                            'font-weight': 'bold',
                            'font-color': 'black',
                            'font-size': 20,
                            'textAlign': 'center'})]),
      
       dbc.Row([dbc.Col(html.Div([
               html.Label(children='Exercise induced angina:'),
               dcc.Dropdown(
                   options=[
                       {'label': 'No', 'value': 0.0},
                       {'label': 'Yes', 'value': 1.0}
                   ],
                   value= 1,
                   id='exang'
               )]), 
               width={'size': 3})],style={'padding': '10px 10px'}),
       dbc.Row([dbc.Col(html.Div([
               html.Label(children='ST depression: '),
               dcc.Input(
                   id='oldpeak',
                   type="number",
                   debounce=True,
                   value= 1.5
               )]), 
               width={'size': 3})],style={'padding': '10px 10px'}),
       dbc.Row([dbc.Col(html.Div([
               html.Label(children='ST slope: '),
               dcc.Dropdown(
                   options=[
                       {'label': 'Upsloping', 'value': 1.0},
                       {'label': 'Flat slope', 'value': 2.0},
                       {'label': 'Downsloping', 'value': 3.0}
                   ],
                   value= 2,
                   id='slope'
               )]),
               width={'size': 3})],style={'padding': '10px 10px'}),
         
        
   dbc.Row([html.Div("Nuclear Medicine results",
                    style={
                               'font-weight': 'bold',
                               'font-color': 'black',
                               'font-weight': 'bold',
                               'font-size': 20,
                               'textAlign': 'center'})]),
       dbc.Row([dbc.Col(html.Div([
               html.Label(children='Affected vessels: '),
               dcc.Input(
                   id='ca',
                   type="number",
                   debounce=True,
                   value= 0
                  )]),
               width={'size': 3})],style={'padding': '10px 10px'}), 
       dbc.Row([dbc.Col(html.Div([
               html.Label(children='Thal Blood flow: '),
               dcc.Dropdown(
                   options=[
                       {'label': 'Normal', 'value': 3.0},
                       {'label': 'Fixed Defect', 'value': 6.0},
                       {'label': 'reversible Defect', 'value': 7.0},
                   ],
                   value= 6,
                   id='thal'
               )]),
               width={'size': 3})],style={'padding': '10px 10px'}),
                      
],style=screen)])

@app.callback(
    Output(component_id='patient_data',component_property="children"),
    [Input('age', 'value'),
     Input('sex', 'value'),
     Input('cp', 'value'),
     Input('trestbps', 'value'),
     Input('chol', 'value'),
     Input('fbs', 'value'),
     Input('restecg', 'value'),
     Input('thalach', 'value'),
     Input('exang', 'value'),
     Input('oldpeak', 'value'),
     Input('slope', 'value'),
     Input('ca', 'value'),
     Input('thal', 'value')]
)
def predict(age, sex,
            cp, trestbps,
            chol, fbs,
            restecg, thalach,
            exang, oldpeak,
            slope, ca, thal):

    df = pd.DataFrame(
        data=[[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]],
        columns=['age', 'sex','cp', 'trestbps','chol', 'fbs','restecg', 'thalach','exang', 'oldpeak',
            'slope', 'ca', 'thal']
    )
    
    # folder = os.path.dirname(__file__)
    # model= load(os.path.join(folder,'finalized_hd_model.pkl'))
    prediction = model.predict(df)
    #y_pred = model.predict_proba(df)[:, 1]*100
    # text_pred = str(np.round(y_pred[0], 1)) + "%"
    
    # assign a risk group
    
    if prediction<=1: risk_grp = 'LOW RISK '
    elif prediction<4: risk_grp = 'MEDIUM RISK '
    else: prediction = 'HIGH RISK '
       
    rg_actions = {
        'LOW RISK ':    ['Discuss possible behavioural changes. Follow-up in 12 months'],
        'MEDIUM RISK ': ['Discuss lifestyle changes, possible referral to RACPC. ' \
                        'Schedule follow-up in 3 months ' \
                        'Additional non-invasive testing is recommended for f/u'],
        'HIGH RISK ':   ['Refer to RACPC, discuss the need for further investigation, '
                        'lifestyle changes and medication.']}
    next_action = rg_actions[risk_grp][0]
    
    result =f"Based on the patient's profile, the predicted likelihood of developing heart disease is {prediction}. " \
         f"This patient is in the {risk_grp} group."\
             f"we would recomend to: {next_action} "
    
    
    return result

if __name__ == '__main__':
    app.run_server()