import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly.tools import mpl_to_plotly
import matplotlib.pyplot as plt
import Colombia
import Metodos

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# Grafica de infectados por dia
infec = plt.figure(figsize=(13, 5))
ax = infec.add_subplot(111)
ax.plot(Colombia.tiempoInfectadosD, Colombia.infectadosD, 'o')
ax.plot(Colombia.tiempoInfectadosT, Colombia.infectadosT, '.r')
ax.plot(Colombia.tiempoInfectadosD, Metodos.modeloExp(Colombia.tiempoInfectadosD, *Colombia.paramsInfect))
plotly_figInfectados = mpl_to_plotly(infec)

# gráfica de recuperados por día
recu = plt.figure(figsize=(13, 5))
axR = recu.add_subplot(111)
axR.plot(Colombia.tiempoRecuperados, Colombia.recuperados, 'o')
plotly_figRecuperados = mpl_to_plotly(recu)

# Gráfica de fallecidos por día
fall = plt.figure(figsize=(13, 5))
axF = fall.add_subplot(111)
axF.plot(Colombia.tiempoFallecidos, Colombia.fallecidos, 'o')
plotly_figFallecidos = mpl_to_plotly(fall)

# Gráfica de recuperados acumulados
acumRecu = plt.figure(figsize=(13, 5))
aR = acumRecu.add_subplot(111)
aR.plot(Colombia.tiempoRecuperados, Colombia.acumuladosR, '--')
plotly_figAcumRecuperados = mpl_to_plotly(acumRecu)

# Gráfica de fallecidos acumulados
acumFall = plt.figure(figsize=(13, 5))
aF = acumFall.add_subplot(111)
aF.plot(Colombia.tiempoFallecidos, Colombia.acumuladosF, '--')
plotly_figAcumFallecidos = mpl_to_plotly(acumFall)


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

    html.Div(children='Infectados por día', style={
        'textAlign': 'center',
        'color': colors['text']
        }
     ),

    dcc.Graph(id='infectados',
              figure=plotly_figInfectados
              ),

    html.Div(children='Recuperados por día', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(id='recuperados',
              figure=plotly_figRecuperados
              ),

    dcc.Graph(
        id='acumRecuperados',
        figure=plotly_figAcumRecuperados
    ),

    html.Div(children='Fallecidos por día', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(id='fallecidos',
              figure=plotly_figFallecidos
              ),

    dcc.Graph(
        id='acumFallecidos',
        figure=plotly_figAcumFallecidos
    ),
])

# Cargar página
if __name__ == '__main__':
    app.run_server(debug=True)
