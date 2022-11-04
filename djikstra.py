from multiprocessing.sharedctypes import Value
from flask import Flask, render_template, request
from vertex import vertices
import networkx as nx
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")
    
@app.route('/result', methods=['GET'])
def result():
    def VisualizarGrafo(grafo):
        G = nx.DiGraph()
        G.add_edges_from(grafo)
        nx.draw_networkx(G, with_labels=True, node_size = 100)
        plt.show()


    def adiciona(grafo_arestas, chave, lista_valores):  # função que adiciona os elementos inicialmente
        if chave not in grafo_arestas:
            grafo_arestas[chave] = list()
        grafo_arestas[chave].update(lista_valores)  # sempre atualizando
        return grafo_arestas


    def dijkstra(grafo, comeco, final):  # algoritmo de dijkstra
        distancia = {}  # Dicionario para mudança e obtenção dos pesos
        fila = []  # Fila dos elementos que ainda não foram visitados
        vistoria = {}  # Observar os caminhos

        for vertice in grafo.keys():
            fila.append(vertice)  # inclui os vertices nos não visitados
            distancia[vertice] = float('inf')  # inicia os caminhos como infinito
        atual = comeco  # atual elemento
        elem_atual = {}  # dicionario com o atual elemento para manipulação e observação
        elem_atual[atual] = 0  # começo com o caminho de peso 0

        distancia[atual] = [0, comeco]
        fila.remove(atual)

        while fila:
            for vizinho, peso in grafo[atual].items():
                soma = peso + elem_atual[atual]  # calculo do peso
                if distancia[vizinho] == float("inf") or distancia[vizinho][0] > soma:
                    distancia[vizinho] = [soma, atual]
                    vistoria[vizinho] = soma

            if vistoria == {}:  # se a vistoria não tiver nenhum caminho, o código parará
                break
            menor = min(vistoria.items(), key=lambda x: x[1])  # seleciona o menor vizinho para progredir
            atual = menor[0]
            elem_atual[atual] = menor[1]
            fila.remove(atual)
            del vistoria[atual]
            
        caminho = Caminho(distancia, comeco, final)
        return distancia[final][0], caminho
        #print(f"Passando por: {Caminho(distancia, comeco, final)}")


    def Caminho(distancias, inicio, final):
        if final != inicio:
            return f"{Caminho(distancias, inicio, distancias[final][1])} -- > {final}"
        else:
            return inicio


    ##Código Principal##
    arestas = dict()
    grafo = []
    for vertice in vertices:
        arestas[vertice] = {}

    try:
        arquivo = open("DADOS.txt", "r", encoding='UTF-8-sig')  # acessando o arquivo
        with arquivo:
            for line in arquivo:
                origem, destino, peso = line.split('-') 
                peso = float(peso)
                grafo.append([origem, destino])
                grafo.append([destino, origem])

                arestas = adiciona(arestas, origem, {destino: peso})  # adicionando a aresta no dicionario
                arestas = adiciona(arestas, destino,
                                {origem: peso})  # adicionando o oposto da aresta no dicionario (ida e volta)


    except FileNotFoundError as msg:
        print(msg)

    origem = request.args.get('origem').strip().lower()
    destino = request.args.get('destino').strip().lower()
    distancia, caminho = dijkstra(arestas, origem, destino)
    grafico = VisualizarGrafo(grafo)

    return render_template("result.html", origin=origem, dest=destino, distance=distancia, route=caminho, plot=grafico)



app.run(debug=True)