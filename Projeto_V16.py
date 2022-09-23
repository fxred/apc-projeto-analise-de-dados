# Importação de bibliotecas
import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import sys

cores = { # Define as cores de alguns elementos que serão usadas posteriormente
    'plano_de_fundo': '#111111',
    'texto': '#D8D8D8'
}

# Variáveis de listas usadas nos filtros
anos = ["Todos", "2016", "2017", "2018", "2019", "2020", "2021"]

#Estruturação da Página
pag = dash.Dash(__name__)
pag.css.append_css({'external_url': '/Assets/Style.css'})
pag.layout = html.Div([
    html.H1('Base de Dados: Criptomoedas'),

    html.H4('Comparação do Bitcoin ao dólar a partir de 2016'),
    dcc.Graph(id = "grafico1"),
    html.Div([
        dcc.RangeSlider(
                id = 'filtro1',
                min=2016,
                max=2021,
                step=None,
                value=[2016, 2021],
                marks={2016: '2016', 2017: '2017', 2018: '2018', 2019: '2019',2020: '2020', 2021: '2021'}
        )
    ]),

    html.H4('Comparação do Bitcoin com outras criptomoedas a partir de 2016'),
    html.Div([
        dcc.Dropdown(
                id = 'filtro2',
                options = [{'label':ano, 'value': ano} for ano in anos],
                value = 'Todos',
                clearable = False,
                style = {'cursor':'pointer'}
        )
    ],
    className = 'drop' # Atributos definidos no CSS quanto à posição do dropdown
    ),
    dcc.Graph(id = "grafico2"),

    html.H4('Transações em dólar do Bitcoin a partir de 2016'),
    html.Div([
        dcc.Dropdown(
            id = 'filtro3',
            options = [{'label':ano, 'value': ano} for ano in anos],
            value = 'Todos',
            clearable = False,
            style = {'cursor':'pointer'}
        )
    ],
    className = 'drop' # Um dos recursos do CSS
    ),
    dcc.Graph(id = "grafico3"),

    html.H4('Transações brutas diárias de Bitcoin desde 2016'),
    html.Div([
    dcc.Dropdown(
        id = 'filter',
        options = [{'label':ano, 'value': ano} for ano in anos],
        value = 'Todos',
        clearable = False,
        style = {'cursor':'pointer'}
        ),
        
    ],
    className = 'drop'
    ),
    dcc.Graph(id = "grafico"),

    html.H4('Quantidade total de Bitcoins em circulação'),
    dcc.Graph(id= "grafico5"),
    html.Div([
        dcc.Slider(
        id= "filtro5",
        min= 2009,
        max= 2021,
        marks={i: '{}'.format(i) for i in range(2009,2022)},
        value=2015
    )
    ]),
])

# ------ Gráfico 1 ------ #

btc_csv = pd.read_csv("BTC-USD.csv", sep=',')
btc_array = btc_csv.values
btc_array_2016 = btc_array[471:] # Filtra o array a partir do primeiro dia de 2016 

b = sys.getsizeof(btc_array_2016)

print(b)

print(btc_array_2016)

datas = []
open_usd = []
high_usd = []
low_usd = []
close_usd = []

for lista in btc_array_2016:
    datas.append(lista[0])
    open_usd.append(lista[1])
    high_usd.append(lista[2])
    low_usd.append(lista[3])
    close_usd.append(lista[4])


@pag.callback(
    Output(component_id='grafico1', component_property= 'figure'),
    Input(component_id='filtro1', component_property='value'),
)

def create_figure(ano):

    datas_v, open_v, high_v, low_v, close_v = [], [], [], [], []

    for data in datas:
        ano1 = data.split('-')
        posicao_data = datas.index(data)
        n = int(ano1[0])
        if ano[0] <= n <= ano[1]:
            datas_v.append(data)
            open_v.append(open_usd[posicao_data])
            high_v.append(high_usd[posicao_data])
            low_v.append(low_usd[posicao_data])
            close_v.append(close_usd[posicao_data])
        

    dados_grafico_1 = go.Candlestick( # Método do Plotly para definir os principais atributos ao gráfico
	x = datas_v,
	open = open_v,
    high = high_v,
    low = low_v,
    close = close_v)

    grafico1 = go.Figure(dados_grafico_1) # Método do Plotly para inserir os atributos da variável "dados_grafico_1" num gráfico
    grafico1.update_layout(
    xaxis_rangeslider_visible = False,
    plot_bgcolor = cores['plano_de_fundo'],
    paper_bgcolor = cores['plano_de_fundo'],
    font_color = cores['texto'],
    height = 650,
    xaxis_title = dict(
        text='<b>Tempo<b>'
    ),
    xaxis = dict(
    tickmode = 'array', # Tick é uma maneira de ditar os valores que vão aparecer ou não nos eixos X e Y
    tickvals = [2016, 2017, 2018, 2019, 2020, 2021],
    ticktext = ['2016', '2017', '2018', '2019', '2020', '2021']
    ),
    yaxis_title = dict(
        text = '<b>Valor em dólar (US$)<b>'
    ))
    
    return grafico1

# --------- Gráfico 2 --------- #

Bitcoin = pd.read_csv('bitcoin_usd.csv', sep = ',')
array_btc = Bitcoin.values
array_btc = array_btc[1993:]

Ethereum = pd.read_csv('ethereum_usd.csv', sep = ',')
array_eth = Ethereum.values

MDash = pd.read_csv('dash_usd.csv', sep = ',')
array_dash = MDash.values

Maker = pd.read_csv('maker_usd.csv', sep = ',')
array_maker = Maker.values

data_btc, data_eth, data_dash, data_maker = [], [], [], []
valor_btc, valor_eth, valor_dash, valor_maker =  [], [], [], []

for lista in array_btc:
	data_btc.append(lista[1])
	valor_btc.append(lista[2])

for lista in array_eth:
    data_eth.append(lista[1])
    valor_eth.append(lista[2])

for lista in array_dash:
    data_dash.append(lista[1])
    valor_dash.append(lista[2])

for lista in array_maker:
    data_maker.append(lista[1])
    valor_maker.append(lista[2])

@pag.callback(
    Output(component_id='grafico2', component_property= 'figure'), # Define-se o id de saída e seu tipo
    Input(component_id='filtro2', component_property='value'), # Definine-se o id do filtro e seu tipo
)

def create_figure(ano):

    btc_f, eth_f, dash_f, maker_f = [], [], [], []
    btc_v, eth_v, dash_v, maker_v = [], [], [], []

    if ano != 'Todos':
        for x in data_btc:
            y = x.split('-')
            if y[0] == ano:
                z = data_btc.index(x)
                btc_f.append(x)
                btc_v.append(valor_btc[z])
        for x in data_eth:
            y = x.split('-')
            if y[0] == ano:
                z = data_eth.index(x)
                eth_f.append(x)
                eth_v.append(valor_eth[z])
        for x in data_dash:
            y = x.split('-')
            if y[0] == ano:
                z = data_dash.index(x)
                dash_f.append(x)
                dash_v.append(valor_dash[z])
        for x in data_maker:
            y = x.split('-')
            if y[0] == ano:
                z = data_maker.index(x)
                maker_f.append(x)
                maker_v.append(valor_maker[z])
    else:
        btc_f = data_btc
        btc_v = valor_btc

        eth_f = data_eth
        eth_v = valor_eth

        dash_f = data_dash
        dash_v = valor_dash

        maker_f = data_maker
        maker_v = valor_maker

    grafico2_btc = go.Scatter(
        x = btc_f,
        y = btc_v,
        mode = 'lines',
        name = 'Bitcoin',
        marker_color = '#E5FF00'
    )

    grafico2_eth = go.Scatter(
        x = eth_f,
        y = eth_v,
        mode = 'lines',
        name = 'Ethereum',
        marker_color = '#F76FFF'
    )

    grafico2_dash = go.Scatter(
        x = dash_f,
        y = dash_v,
        mode = 'lines',
        name = 'Dash', 
        marker_color = '#00FA43'
    )

    grafico2_maker = go.Scatter(
        x = maker_f,
        y = maker_v,
        mode = 'lines',
        name = 'Maker',
        marker_color = '#3EE3FF'
    )

    grafico2 = go.Figure(data = [
        grafico2_btc, grafico2_eth, grafico2_dash, grafico2_maker
    ])

    grafico2.update_layout(
        yaxis_title = dict(text='<b>Valores em dólar (US$)<b>'),
        xaxis_title = dict(text='<b>Tempo<b>'),
        plot_bgcolor = cores['plano_de_fundo'],
        paper_bgcolor = cores['plano_de_fundo'],
        font_color = cores['texto'],
        height = 650,
        xaxis = dict(
        tickmode = 'array',
        tickvals = [2016, 2017, 2018, 2019, 2020, 2021],
        ticktext = ['2016', '2017', '2018', '2019', '2020', '2021']
        )
    )

    return grafico2

# ------ Gráfico 3 ------ #

tran_usd_csv = pd.read_csv('tran_usd_btc.csv', sep=',')
array_tran_usd = tran_usd_csv.values

data_tran = []
tran_usd = []

for lista in array_tran_usd:
    data_tran.append(lista[0])
    tran_usd.append(lista[1])

@pag.callback(
    Output(component_id='grafico3', component_property= 'figure'), # Define-se o id de saída e seu tipo
    Input(component_id='filtro3', component_property='value'), # Definine-se o id do filtro e seu tipo
)

def create_figure(ano):
    btc_f = []
    btc_v= []
    if ano != 'Todos':
        for x in data_tran:
            y = x.split('-')
            z = data_tran.index(x)
            if y[0] == ano:
                btc_f.append(x)
                btc_v.append(tran_usd[z])
    else: 
        btc_f = data_tran
        btc_v = tran_usd

    fig = go.Scatter(
        x = btc_f,
        y = btc_v,
        marker_color = '#19C2FF',
        mode = 'lines',
        name = '',
        hovertemplate = '%{y} dólares' + '<br>' + '%{x}'
    )

    grafico3 = go.Figure(fig)
    grafico3.update_layout(
        plot_bgcolor = cores['plano_de_fundo'],
        paper_bgcolor = cores['plano_de_fundo'],
        font_color = cores['texto'],
        height = 650,
        xaxis_title = dict(text = '<b>Tempo<b>'),
        xaxis1 = dict(
            rangeslider=dict(visible=True), #Um filtro do próprio Plotly
            linecolor = 'rgb(63, 64, 63)', #Cor da linha do eixo X
            linewidth = 2, #Espessura da linha do eixo X

        ),
        yaxis_title = dict(text = '<b>Transações em dólar (US$)<b>'),
        xaxis = dict(
            tickmode = 'array',
            tickvals = [2016, 2017, 2018, 2019, 2020, 2021],
            ticktext = ['2016', '2017', '2018', '2019', '2020', '2021']
        ),
        yaxis = dict(
            type = 'log'
        )
    )
    return grafico3

# ------ Gráfico 4 ------ #

transacao = pd.read_csv('tran_usd_btc.csv', sep =',')
transacao_array = transacao.values
datas = []
valores = []

for lista in transacao_array:
	datas.append(lista[0])
	valores.append(lista[1])

@pag.callback(

    Output(component_id = 'grafico', component_property = 'figure'),
    Input(component_id = 'filter', component_property = 'value'),

)
def create_figure(ano):

    btc_f = []
    btc_v = []

    if ano != 'Todos':

        for x in datas:
            y = x.split('-')
            z = datas.index(x)
            if y[0] == ano:
                btc_f.append(x)
                btc_v.append(valores[z])
    else:

        btc_f = datas
        btc_v = valores

    figura = go.Bar(
        x = btc_f,
        y = btc_v,
    )

    grafico4 = go.Figure(figura)

    grafico4.update_layout(
        plot_bgcolor = cores['plano_de_fundo'],
        paper_bgcolor = cores['plano_de_fundo'],
        font_color = cores['texto'],
        xaxis = dict(
        tickmode = 'array',
        tickvals = [2016, 2017, 2018, 2019, 2020, 2021],
        ticktext = ['2016', '2017', '2018', '2019', '2020', '2021']
        ),
        yaxis_title=dict(text='<b>Transações brutas em dólar<b>'),
        xaxis_title=dict(text='<b>Data<b>'),
        height = 650,
        yaxis = dict(type = 'log')
    )

    return grafico4

# ------ Gráfico 5 ------ #

dados = pd.read_csv('total-bitcoins.csv', sep=',')
arquivo=dados.values

tempo=[]
quantidade=[]

for lista in arquivo:
    tempo.append(lista[0])
    quantidade.append(lista[1])

@pag.callback(
    Output(component_id='grafico5', component_property= 'figure'), # Define-se o id de saída e seu tipo
    Input(component_id='filtro5', component_property='value'), # Definine-se o id do filtro e seu tipo
)    

def grafico (ano):
    tempo2=[]
    quantidade2=[]

    for x in tempo:
        ano2= x.split('-')
        posicao= tempo.index(x)
        z= int(ano2[0])
        if z <= ano:
            tempo2.append(x)
            quantidade2.append(quantidade[posicao])

    g1 = go.Scatter(
        x = tempo2,
        y = quantidade2,
        name = '',
        marker_color = '#90FF00',
        fill = 'tozeroy', # Tipo de gráfico que preenche o plano abaixo da linha
        hovertemplate = '%{y} Bitcoins' + '<br>' + '%{x}'

)
    grafico5 = go.Figure(g1)

    grafico5.update_layout(
        plot_bgcolor = cores['plano_de_fundo'],
        paper_bgcolor = cores['plano_de_fundo'],
        font_color = cores['texto'],
        xaxis_title = dict(
            text = '<b>Tempo<b>'
    ),

        height = 650,
        yaxis_title = dict(
            text = '<b>Quantidade de Bitcoins cumulativa<b>',
    ),
        
)
    return grafico5        

# ------ Lançamento da página ------ #
if __name__ == '__main__':
    pag.run_server(debug=True) # Comando para rodar a página