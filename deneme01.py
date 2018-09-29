# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
#import numpy as np
#import datetime as dt
import io
import base64

##df = pd.read_excel('/Users/zozgur/Dropbox/D4C/Isler/Unilever-Knorr/knorrexample2.xlsx')

app = dash.Dash()

app.layout = html.Div(children=[
    
    html.H1(children='Unilever Veri Analizi',
            style={
            'textAlign': 'center'
            }
            
    ),
    
    html.H2('Veri dosyanızı yükleyiniz:',
            style={
            'textAlign': 'center'
            }
    ),
    
    dcc.Upload(
        id='upload',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),

    html.Div(
        children='', 
        id='upload_info-div'
    ),
       
    dcc.Graph(
        id='whole-graph',
        figure = {}
    ),

])


@app.callback(
    Output('upload_info-div', 'children'),
    [Input('upload', 'filename')])
def update_file_info(filename):
    if 'csv' in filename:
        return filename + " uploaded!"
    elif 'xls' in filename or 'xlsx' in filename:
        return filename + " uploaded!"  
    else:
        return "Please upload a CSV or EXCEL file!"
             
@app.callback(
    Output('whole-graph', 'figure'),
    [Input('upload', 'contents'),
     Input('upload', 'filename')])
def update_figure(contents, filename):
    content_type, content_string = contents.split(',')
    
    decoded = base64.b64decode(content_string)
    
    if 'csv' in filename:
            # Assume that the user uploaded a CSV file
        df2 = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        df2['time'] = pd.to_datetime(df['time'])
    elif 'xls' in filename or 'xlsx' in filename:
            # Assume that the user uploaded an excel file
        df2 = pd.read_excel(io.BytesIO(decoded))
        df2['time'] = pd.to_datetime(df['time'])
    else:
        return
    
    figure = {
                'data': [
                    {'x': df2['time'], 'y': df2['weight'], 'mode': 'markers',
                    'marker': {'size': 2}, 'name': 'Weights'},
                ],
                'layout': {
                        'title': 'Bir günlük ağırlık ölçümleri'
                }
    }
    
    return figure



                

if __name__ == '__main__':
    app.run_server(debug=True)
