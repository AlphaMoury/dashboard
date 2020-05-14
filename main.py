import dash
import dash_core_components as dcc
import dash_html_components as html
import datos

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
                {'x': ['Infectados', 'Recuperados', 'Fallecidos', 'Total'], 'y': [datos.i, datos.r, datos.f, datos.N],
                 'type': 'bar', 'name': 'IRFT'},
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
            html.Tr([html.Td(datos.i, style={
                'textAlign': 'center',
                'color': colors['text']
            }),
             html.Td(datos.r, style={
                'textAlign': 'center',
                'color': colors['text']
            }),
             html.Td(datos.f, style={
                'textAlign': 'center',
                'color': colors['text']
            }),
             html.Td(datos.N, style={
                'textAlign': 'center',
                'color': colors['text']
            })])
        ]),
    ]),

    html.Div(children='COVID-19 por Género', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='bar genero',
        figure={
            'data': [
                {
                    'labels': ['Femenino', 'Masculino', 'Otro'],
                    'values': [datos.femenino, datos.masculino, datos.otro],
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

    html.Div(children='Fecha-Estado', style={
            'textAlign': 'center',
            'color': colors['text']
    }),

    dcc.Graph(
        id='fech-est',
        figure= {
            'data': [
                {'x': datos.datos['Fecha de notificación'], 'y': datos.datos['ID de caso'],
                 },
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

])

# Cargar página
if __name__ == '__main__':
    app.run_server(debug=True)
