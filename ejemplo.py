import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Tutoriales Dash en AprenderPython.com'),
    dcc.Graph(id='ejemplo', figure={
        'data': [
            {'x': [1, 2, 3, 4], 'y': [1, 8, 3, 7], 'type': 'line', 'name': 'Bicicletas'},
            {'x': [1, 2, 3, 4], 'y': [5, 2, 8, 8], 'type': 'bar', 'name': 'Bicicletas electricas'},
        ],
        'layout': {
            'title': 'Ejemplo básico en Dash'
        }
    })
])

if __name__ == '__main__':
    app.run_server(debug=True)
