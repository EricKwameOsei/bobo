### SOLUTION TO AUDIOSR MANAGER
import plotly.express as px
import dash_bootstrap_components as dbc
import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
from datetime import datetime
import time
import csv
from matplotlib import pyplot as plt

colnames=["DATE","TIME","GPU","THREAD","ffimagestream","ID","INPUT","STREAM","STATUS","HTTP","POINT","AUDIOSR"] 
#df=pd.read_table("/home/eric.kwame/Downloads/report_sevilla_fc.csv",sep='\s+',on_bad_lines='skip',names=colnames, header=None)
#df=pd.read_table("/home/eric.kwame/askiaDash/file1.csv",sep='\s+',on_bad_lines='skip',names=colnames, header=None)
df=pd.read_table("file1.csv",sep='\s+',on_bad_lines='skip',names=colnames, header=None)



#df=pd.read_table("/home/EricKwame/mysite/data/file.csv",sep='\s+',on_bad_lines='skip',names=colnames, header=None)

df1=df[['DATE','TIME','THREAD','ID','POINT','AUDIOSR','STATUS']]
df1['DATE'] = df1['DATE'].str.replace(r'0m', '')
df1['DATE'] = df1['DATE'].str.replace(r'[', '')
df1['POINT'] = df1['POINT'].str.replace(r's', '')
df1['POINT'] = df1['POINT'].str.replace(r'-', '')
df1['POINT'] = df1['POINT'].str.replace(r's', '')
df1['POINT'] = df1['POINT'].str.replace(r',', '')
df1['ID'] = df1['ID'].str.replace(r')', '')
df1['ID'] = df1['ID'].str.replace(r'(', '')
df1['POINT'] = df1['POINT'].str.replace(r'delay:', '')
df1['AUDIOSR'] = df1['AUDIOSR'].str.replace(r'audioSR:0,Syncing:1}', '')
df1['AUDIOSR'] = df1['AUDIOSR'].str.replace(r'}', '')
df1['AUDIOSR'] = df1['AUDIOSR'].str.replace(r'audioSR:48000,Syncing:0', '')
df1['AUDIOSR'] = df1['AUDIOSR'].str.replace(r'audioSR:48000,Syncing:1', '')
df1['AUDIOSR'] = df1['AUDIOSR'].str.replace(r'audioSR:-1246405708,Syncing:1', '')
df1['AUDIOSR'] = df1['AUDIOSR'].str.replace(r'audioSR:0,Syncing:0', '')
df1['DATE'] = df1['DATE'].str.replace(r'\x1b', '')
df1["YEAR"]=pd.to_datetime(df1['DATE'] + ' ' + df1['TIME'])
df1['AUDIOSR'] = pd.to_numeric(df1['AUDIOSR'], errors='coerce')
df1['POINT'] = pd.to_numeric(df1['POINT'], errors='coerce')
status_data=df1[df1['STATUS']=="status:"]
status_data_unique=status_data["ID"].unique()
params_data=df1[df1['STATUS']=="params:"]
params_data=params_data[params_data['POINT'] < 7]
params_data_unique=params_data["ID"].unique()


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([
    
    html.H1(id = 'H1', children = 'Camera Anomaly Detection App', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),
    
       dbc.Card([
                dbc.CardBody([
                              html.Center(html.H1("cinfo Camera", className='card-title')),
                            ])
              ],
              color='red', 
              inverse=True,
              style={
                  "width":"180rem",
                  "margin-left":"1rem",
                  "margin-top":"1rem",
                  "margin-bottom":"1rem"
                  }
            ),   
    
    
    
    dcc.Dropdown(
        id='demo-dropdown',
        options=[{'label': k, 'value': k} for k in status_data_unique],
        value=[],
        multi=True
    ),
    
    html.Hr(),
    dcc.Graph(id='display-selected-values'),
    
    dcc.Dropdown(
        id='demo-dropdown1',
        options=[{'label': a, 'value': a} for a in params_data_unique],
        value=[],
        multi=True),
    

    
    html.Hr(),
    dcc.Graph(id='display-selected-values1'),

])

@app.callback(
    dash.dependencies.Output('display-selected-values', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    ts = status_data[status_data["ID"].isin(value)]
    fig = px.line(ts, x="YEAR", y="AUDIOSR", color="ID")
    
    fig.update_layout(
      title="Input Stream Status ",title_x=0.5, 
      yaxis_title="Status", 
      xaxis_title="Period", 
      font=dict(
          family="Courier New, monospace", 
          color="RebeccaPurple", 
          size=12 
      )
  )
    
    return fig 

@app.callback(
    dash.dependencies.Output('display-selected-values1', 'figure'),
    [dash.dependencies.Input('demo-dropdown1', 'value')])
def update_output(value):
    ts = params_data[params_data["ID"].isin(value)]
    fig = px.line(ts, x="YEAR", y="POINT", color="ID")
    
    fig.update_layout(
      title="Input Stream Params",title_x=0.5, 
      yaxis_title="Params", 
      xaxis_title="Period", 
      font=dict(
          family="Courier New, monospace", 
          color="RebeccaPurple", 
          size=12
      )
  )
  
                     
                                       
                     
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True,port=9525)
