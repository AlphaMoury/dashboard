import dash
import dash_core_components as dcc
import dash_html_components as html
import Colombia

# import plotly.plotly as py

# from plotly.graph_objs import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='COVID-19 Colombia',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Un dashboard del COVID-19', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='bar IRF',
        figure={
            'data': [
                {'x': ['Fallecidos', 'Recuperados', 'Infectados', 'Total'],
                 'y': Colombia.FRI,
                 'type': 'bar', 'name': 'FRI'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),

    html.Table([
        html.Thead(
            html.Tr([html.Th('Infectados', style={
                'textAlign': 'center',
                'color': colors['text']
            }),
                     html.Th('Recuperados', style={
                         'textAlign': 'center',
                         'color': colors['text']
                     }),
                     html.Th('Fallecidos', style={
                         'textAlign': 'center',
                         'color': colors['text']
                     }),
                     html.Th('Total', style={
                         'textAlign': 'center',
                         'color': colors['text']
                     })])
        ),
        html.Tbody([
            html.Tr([html.Td(Colombia.FRI[2], style={
                'textAlign': 'center',
                'color': colors['text']
            }),
                     html.Td(Colombia.FRI[1], style={
                         'textAlign': 'center',
                         'color': colors['text']
                     }),
                     html.Td(Colombia.FRI[0], style={
                         'textAlign': 'center',
                         'color': colors['text']
                     }),
                     html.Td(Colombia.FRI[3], style={
                         'textAlign': 'center',
                         'color': colors['text']
                     })])
        ]),
    ]),

    html.Div(children='Estado en gráfica torta', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='pie FRI',
        figure={
            'data': [
                {
                    'labels': ['Fallecido', 'Recuperado', 'Infectado'],
                    'values': [Colombia.FRI[0], Colombia.FRI[1], Colombia.FRI[2]],
                    'type': 'pie',
                }
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                },
            }
        }
    ),

    html.Div(children='Género', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='pie genero',
        figure={
            'data': [
                {
                    'labels': ['Femenino', 'Masculino', 'Otro'],
                    'values': [Colombia.gen[0], Colombia.gen[1], Colombia.gen[2]],
                    'type': 'pie',
                }
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                },
            }
        }
    ),
])

# Cargar página
if __name__ == '__main__':
    app.run_server(debug=True)
