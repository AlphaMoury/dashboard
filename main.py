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
    mode='markers',
    name='Por día')
datos = go.Scatter(
    x=Colombia.tiempoInfectadosD,
    y=Colombia.infectadosD,
    name='Datos',
    mode='markers',)
datos_test = go.Scatter(
    x=Colombia.tiempoInfectadosT,
    y=Colombia.infectadosT,
    name='Datos_test',
    mode='markers',)
regresion = go.Scatter(
    x=Colombia.tiempoInfectadosD,
    y=Metodos.modeloExp(Colombia.tiempoInfectadosD, *Colombia.paramsInfect),
    name='Regresión')
acumulados = go.Scatter(
    x=Colombia.tiempoInfectados,
    y=Colombia.acumuladosI,
    mode='markers',
    name='Acumulados'
)

figInfec = make_subplots(rows=1, cols=2,
                         subplot_titles=(
                             'Infectados por día',
                             'Infectados Acumulados'))

figInfec.add_trace(Infec, 1, 1)
figInfec.add_trace(acumulados, 1, 2)

figInfec.update_xaxes(title_text='Tiempo(Días)')
figInfec.update_yaxes(title_text='Número personas')
figInfec.update_layout(title='Gráficas de infectados')

layout = go.Layout(title='Datos y regresión',
                   xaxis={'title': 'Tiempo(Días)'},
                   yaxis={'title': 'Número de personas'},
                   hovermode='closest'
                   )

figInfectReg = go.Figure(data=[datos, datos_test, regresion], layout=layout)

# ----------------------- Recuperados ----------------------
datos = go.Scatter(
    x=Colombia.tiempoRecuperadosD,
    y=Colombia.recuperadosD,
    name='Datos',
    mode='markers',)
datos_test = go.Scatter(
    x=Colombia.tiempoRecuperadosT,
    y=Colombia.recuperadosT,
    name='Datos_test',
    mode='markers',)
regresion = go.Scatter(
    x=Colombia.tiempoRecuperadosD,
    y=Metodos.modeloExp(Colombia.tiempoRecuperadosD, *Colombia.paramsRecup),
    name='Regresión')

layout = go.Layout(title='Datos y regresión',
                   xaxis={'title': 'Tiempo(Días)'},
                   yaxis={'title': 'Número de personas'},
                   hovermode='closest')

figRecupReg = go.Figure(data=[datos, datos_test, regresion], layout=layout)

# ----------------------- Fallecidos ----------------------
datos = go.Scatter(
    x=Colombia.tiempoFallecidosD,
    y=Colombia.fallecidosD,
    name='Datos',
    mode='markers',)
datos_test = go.Scatter(
    x=Colombia.tiempoFallecidosT,
    y=Colombia.fallecidosT,
    name='Datos_test',
    mode='markers',)
regresion = go.Scatter(
    x=Colombia.tiempoFallecidosD,
    y=Metodos.modeloExp(Colombia.tiempoFallecidosD, *Colombia.paramsFall),
    name='Regresión')

layout = go.Layout(title='Datos y regresión',
                   xaxis={'title': 'Tiempo(Días)'},
                   yaxis={'title': 'Número de personas'},
                   hovermode='closest')

figFallReg = go.Figure(data=[datos, datos_test, regresion], layout=layout)

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
        dcc.Tab(label='Fallecidos', value='tab-fall')
    ]),
    html.Div(id='tabs-content')
])


# --------- Contenido ---------
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_contect(tab):
    if tab == 'tab-gen':
        return html.Div([
            html.H1(
                children='Dashboard COVID-19',
                style={
                    'textAlign': 'center', 'color': colors['text']}),
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
                ),
                }
            ),
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
                })
        ])
    elif tab == 'tab-inf':
        return html.Div([
            html.H2(
                children='Infectados',
                style={'textAlign': 'center', 'color': colors['text']}),
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
                children='Recuperados',
                style={
                        'textAlign': 'center', 'color': colors['text']}),
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
                dcc.Graph(
                    id='regresion-recup', figure=figRecupReg
                )],
                style={'textAlign': 'center', 'color': colors['text']}
            )
        ])
    elif tab == 'tab-fall':
        return html.Div([
            html.H2(
                children='Fallecidos',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }),
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
                    ),
                    }
                ),
                dcc.Graph(
                    id='regresion-fall', figure=figFallReg
                )]
            )
        ])


# Cargar página
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)
