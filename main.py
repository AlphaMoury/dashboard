# encoding: utf-8

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
import Colombia
import Metodos

# ----------------------- Infectados ----------------------
Infec = go.Scatter(
    x=Colombia.tiempoInfectados,
    y=Colombia.infectados,
    mode='markers', name='Por día')
datos = go.Scatter(
    x=Colombia.tiempoInfectadosD,
    y=Colombia.infectadosD,
    name='Datos', mode='markers',)
datos_test = go.Scatter(
    x=Colombia.tiempoInfectadosT,
    y=Colombia.infectadosT,
    name='Datos_test', mode='markers',)
regresion = go.Scatter(
    x=Colombia.tiempoInfectadosD,
    y=Metodos.modeloExp(Colombia.tiempoInfectadosD, *Colombia.paramsInfect),
    name='Regresión', mode='lines')
acumulados = go.Scatter(
    x=Colombia.tiempoInfectados,
    y=Colombia.acumuladosI,
    mode='markers', name='Acumulados')

figInfec = make_subplots(rows=1, cols=2,
                         subplot_titles=('Infectados por día','Infectados Acumulados'))

figInfec.add_trace(Infec, 1, 1)
figInfec.add_trace(acumulados, 1, 2)

figInfec.update_xaxes(title_text='Tiempo(Días)')
figInfec.update_yaxes(title_text='Número personas')
figInfec.update_layout(title='Gráficas de infectados')

layout = go.Layout(title='Datos y regresión Infectados',
                   xaxis={'title': 'Tiempo(Días)'},
                   yaxis={'title': 'Número de personas'},
                   hovermode='closest')

figInfectReg = go.Figure(data=[datos, datos_test, regresion], layout=layout)

# ----------------------- Recuperados ----------------------
datos = go.Scatter(
    x=Colombia.tiempoRecuperadosD,
    y=Colombia.recuperadosD,
    name='Datos', mode='markers',)
datos_test = go.Scatter(
    x=Colombia.tiempoRecuperadosT,
    y=Colombia.recuperadosT,
    name='Datos_test', mode='markers',)
regresion = go.Scatter(
    x=Colombia.tiempoRecuperadosD,
    y=Metodos.modeloExp(Colombia.tiempoRecuperadosD, *Colombia.paramsRecup),
    name='Regresión')

layout = go.Layout(title='Datos y regresión Recuperados',
                   xaxis={'title': 'Tiempo(Días)'},
                   yaxis={'title': 'Número de personas'},
                   hovermode='closest')

figRecupReg = go.Figure(data=[datos, datos_test, regresion], layout=layout)

# ----------------------- Fallecidos ----------------------
datos = go.Scatter(
    x=Colombia.tiempoFallecidosD,
    y=Colombia.fallecidosD,
    name='Datos', mode='markers',)
datos_test = go.Scatter(
    x=Colombia.tiempoFallecidosT,
    y=Colombia.fallecidosT,
    name='Datos_test', mode='markers',)
regresion = go.Scatter(
    x=Colombia.tiempoFallecidosD,
    y=Metodos.modeloExp(Colombia.tiempoFallecidosD, *Colombia.paramsFall),
    name='Regresión')

layout = go.Layout(title='Datos y regresión Fallecidos',
                   xaxis={'title': 'Tiempo(Días)'},
                   yaxis={'title': 'Número de personas'},
                   hovermode='closest')

figFallReg = go.Figure(data=[datos, datos_test, regresion], layout=layout)

# ----------------------- Modelos -----------------------------
suceptibles = go.Scatter(
    x=Colombia.t,
    y=Colombia.sol[:, 0],
    name='Suceptibles', mode='lines')
infectados = go.Scatter(
    x=Colombia.t,
    y=Colombia.sol[:, 1],
    name='infectados', mode='lines')
recuperados = go.Scatter(
    x=Colombia.t,
    y=Colombia.sol[:, 2],
    name='Recuperados y fallecidos', mode='lines')
datos = go.Scatter(
    x=Colombia.t,
    y=Colombia.acumuladosI[35:],
    name='Datos infectados', mode='markers')

layout = go.Layout(title='Modelo SIR',
                   xaxis={'title': 'Tiempo(Días)'},
                   yaxis={'title': 'Número de personas'},
                   hovermode='closest')

figSIR = go.Figure(data=[suceptibles, infectados, recuperados, datos], layout=layout)

# --------------- DASHBOARD -------------------------------------
app = dash.Dash()

# -------- Estilos ---------
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# --------- Tabs contect -----------
app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-gen', children=[
        dcc.Tab(label='General', value='tab-gen'),
        dcc.Tab(label='Infectados', value='tab-inf'),
        dcc.Tab(label='Recuperados', value='tab-recu'),
        dcc.Tab(label='Fallecidos', value='tab-fall'),
        dcc.Tab(label='Modelos', value='tab-model')
    ]),
    html.Div(id='tabs-content')
])


# --------- Contenido ---------
@app.callback(Output('tabs-content', 'children'),[Input('tabs', 'value')])
def render_contect(tab):
    if tab == 'tab-gen':
        return html.Div([
            html.H1(
                children='Dashboard COVID-19',
                style={'textAlign': 'center', 'color': colors['text']}),
            dcc.Graph(
                id='bar-FRI',
                figure={'data': [
                    go.Bar(
                        x=['Fallecidos', 'Recuperados', 'Infectados', 'Total'],
                        y=Colombia.FRI
                    )],
                    'layout': go.Layout(
                        title='Gráfica de Infectados, Fallecidos, Recuperados',
                        xaxis={'title': 'Categorías'},
                        yaxis={'title': 'Número de personas'},
                        hovermode='closest'
                    )
                }),
            dcc.Graph(
                id='pie-gen',
                figure={'data': [
                    go.Pie(
                        labels=['Femenino', 'Masculino', 'Otro'],
                        values=Colombia.gen,
                        hole=.4,
                        textinfo='label+percent'
                    )],
                    'layout':  go.Layout(
                        title='Gráfica de torta por género'
                ),
            }),
            dcc.Graph(
                id='pie-tipo',
                figure={'data': [
                    go.Pie(
                        labels=['Importado', 'Relacionado', 'En estudio'],
                        values=Colombia.IRE,
                        hole=.4,
                        textinfo='label+percent'
                    )],
                    'layout':  go.Layout(
                        title='Gráfica de torta tipo de caso'
                ),
            }),
            dcc.Graph(
                id='bar-edad',
                figure={
                    'data': [
                        go.Bar(
                        x=['0-9','10-19','20-29','30-39','40-49','50-59','60-69','70-79','80-89','90+'],
                        y=Colombia.edad,
                        marker_color=list(range(10))
                    )],
                    'layout': go.Layout(
                        title='Gráfica de Infectados por edades',
                        xaxis={'title': 'Edades'},
                        yaxis={'title': 'Número de personas'},
                        hovermode='closest'
                    )
            })
        ])
    elif tab == 'tab-inf':
        return html.Div([
            html.H2(
                children='Infectados', style={'textAlign': 'center', 'color': colors['text']}),
            html.Div([
                dcc.Graph(
                    id='scatter-infec', figure=figInfec),
                dcc.Graph(
                    id='regresion-infec', figure=figInfectReg)],
                    style={'textAlign': 'center', 'color': colors['text']}
            )
        ])
    elif tab == 'tab-recu':
        return html.Div([
            html.H2(
                children='Recuperados',style={'textAlign': 'center', 'color': colors['text']}),
            html.Div([
                dcc.Graph(
                    id='scatter-recup',
                    figure={'data': [
                            go.Scatter(
                                x=Colombia.tiempoRecuperados,
                                y=Colombia.recuperados,
                                mode='markers',
                                name='Por día'
                            )],
                            'layout': go.Layout(
                                title='Gráfica de recuperados por día',
                                xaxis={'title': 'Tiempo(Días)'},
                                yaxis={'title': 'Número de personas'},
                                hovermode='closest'
                            )}
                ),
                dcc.Graph(id='regresion-recup', figure=figRecupReg)],
                style={'textAlign': 'center', 'color': colors['text']}
            )
        ])
    elif tab == 'tab-fall':
        return html.Div([
            html.H2(
                children='Fallecidos', style={'textAlign': 'center', 'color': colors['text']}),
            html.Div([
                dcc.Graph(
                    id='scatter-fall',
                    figure={'data': [
                        go.Scatter(
                            x=Colombia.tiempoFallecidos,
                            y=Colombia.fallecidos,
                            mode='markers',
                            name='Por día'
                        )],
                        'layout': go.Layout(
                            title='Gráfica de fallecidos por día',
                            xaxis={'title': 'Tiempo(Días)'},
                            yaxis={'title': 'Número de personas'},
                            hovermode='closest'
                    )}
                ),
                dcc.Graph(id='regresion-fall', figure=figFallReg)]
            )
        ])
    elif tab == 'tab-model':
        return html.Div([
            html.H2(
                children='Modelos',
                style={'textAlign': 'center', 'color': colors['text']}),
            html.Div([
                html.H3(
                    children='SIR',
                    style={'textAlign': 'center', 'color': colors['text']}),
                dcc.Graph(id='modelo-SIR', figure=figSIR),
                html.H3(
                    children='Parámetros SIR',
                    style={'textAlign': 'center', 'color': colors['text']}),
                dcc.Graph(
                    id='Parametro-beta',
                    figure={
                        'data': [
                            go.Scatter(
                                x = Colombia.dSdt,
                                y = Colombia.SI,
                                mode='markers+lines',
                                name='SI contra dSdt'
                                )],
                        'layout': go.Layout(
                            title='Cambio de Beta',
                            yaxis={'title': 'SuceptiblesxInfectados'},
                            xaxis={'title': 'Derivada de suceptibles respecto al tiempo'},
                            hovermode='closest'
                            )}
                    ),
                html.P(['Valor de Beta a para la fecha 13 de abril es: ', Colombia.beta]),
                dcc.Graph(
                    id='Parametro-gamma',
                    figure={
                        'data': [
                            go.Scatter(
                                x = Colombia.dRdt,
                                y = Colombia.I,
                                mode='markers+lines',
                                name='SI contra dSdt'
                                )],
                        'layout': go.Layout(
                            title='Cambio de Gamma',
                            yaxis={'title': 'Infectados'},
                            xaxis={'title': 'Derivada de recuperados respecto al tiempo'},
                            hovermode='closest'
                            )}
                    ),
                html.P(['Valor de Gamma a para la fecha 13 de abril es: ', Colombia.gamma])
                ])
        ])

# Cargar página
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)
