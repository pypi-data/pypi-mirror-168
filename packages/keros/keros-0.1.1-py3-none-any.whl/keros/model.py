import random
import numpy as np
from .model_tools import Tools

class MClassifier:
    """
    Info:
        Rede neural baseada no modelo perceptron de multicamadas (Multi-Layer Perceptron - MLP).
        Por enquanto, a rede neural possui apenas uma camada de entrada, uma oculta e uma de saida.

    Functions: 
        fit: Função para treinar a rede neural.
        predict: Função para predizer o resultado da rede neural.
        initialize_weights: Função para inicializar os pesos da rede neural.
    
    """

    def __init__(self):
        #Inicializa listas para armazenar os pesos.
        self._layers = {}
        self._layers_activated = {}
        self._n_layers = 2
        #Inicializa uma variável para armazenar o erro.
        self._mean_absolute_loss = 0
        #Metrics
        self._accuracy = 0
        self._precision = 0
        self._recall = 0
        self._f1 = 0
        self._kappa = 0

    def fit(self, x, y, epoch=5, neurons=5, n_layers=2, learning_rate=0.0001, error_threshold=0.1, moment=1):
        """
        Info: 
            Esta função realiza o treinamento da rede neural.
            A rede será treinada até que o valor máximo para o loss seja atingido,
            até que seja atingido o número de épocas definido.
        Params:
            x (Array numpy): Valores de entrada / features.
            y (array numpy): Rotulos corretamente marcados.
            epoch (int): Valor de epocas de treinamento.
            neurons (int): Representa a quantidade de neuronios.
            n_layers (int): Representa a quantidade de camadas. 
            learning_rate (float): Taxa de aprendizagem da rede.
            error_threshold (float): Valor máximo para o loss.
            moment (float): Otimiza o aprendizado evitantando mínimos locais na curva de erro.
        """
        self.check_params(epoch, neurons, n_layers, learning_rate)

        #--------------------------INICIALIZANDO OS PESOS------------------------------
        self._n_layers = n_layers
        self.initialize_weights(x, neurons, n_layers)
        PREFIX = "Layer-"
        #--------------------------INICIALIZANDO O TREINO------------------------------
        #Percorre o numero de epocas
        for epc in range(epoch):
            #Atribui as features para a camada de entrada
            layer_active = x

            for id_layer in range(n_layers):
                layer = np.dot(layer_active, self._layers[PREFIX + str(id_layer)])
                layer_active = self.sigmoid(layer)
                self._layers_activated[PREFIX + str(id_layer)] = layer_active

            #------------------------CALCULANDO O ERRO---------------------------------
            loss = y - layer_active
            self._mean_absolute_loss = np.mean(np.abs(loss))
            print("Loss: {}".format(self._mean_absolute_loss))

            if self._mean_absolute_loss <= error_threshold:
                y_pred = [[self.thresh(i)] for i in layer_active]
                self._accuracy, self._precision, self._recall, self._f1, self._kappa = Tools.metrics(y, y_pred)
                break
            
            #---------------------ATUALIZANDO OS PESOS-------------------------------
            #Último layer
            derivative_last_layer = self.sigmoid_derivative(self._layers_activated[PREFIX + str(n_layers - 1)])
            delta_last_layer = loss * derivative_last_layer

            #Atualizando os pesos da ultima camada
            activeXdelta = np.dot(self._layers_activated[PREFIX + str(n_layers - 2)].T, delta_last_layer)
            self._layers[PREFIX + str(n_layers - 1)] = (self._layers[PREFIX + str(n_layers - 1)] * moment) + (activeXdelta * learning_rate)

            #Layers ocultos
            for id_layer in range(n_layers - 2, 0, -1):
                delta_last_layer = np.dot(delta_last_layer, self._layers[PREFIX + str(id_layer + 1)].T) * self.sigmoid_derivative(self._layers_activated[PREFIX + str(id_layer)])
                self._layers[PREFIX + str(id_layer)] = (self._layers[PREFIX + str(id_layer)] * moment) + (np.dot(self._layers_activated[PREFIX + str(id_layer - 1)].T, delta_last_layer) * learning_rate)

            #Camada de entrada
            delta_last_layer = np.dot(delta_last_layer, self._layers[PREFIX + str(1)].T) * self.sigmoid_derivative(self._layers_activated[PREFIX + str(0)])
            self._layers[PREFIX + str(0)] = (self._layers[PREFIX + str(0)] * moment) + (np.dot(x.T, delta_last_layer) * learning_rate)

        #-------------------------FIM DO TREINO-------------------------------------------

        #---------------------CALCULANDO MÉTRICAS-----------------------------------------
        y_pred = [[self.thresh(i)] for i in layer_active]
        self._accuracy, self._precision, self._recall, self._f1, self._kappa = Tools.metrics(y, y_pred)
             
    def predict(self, x):
        """
        Info:
            Camada de predição da rede neural.
        Params:
            x (Array numpy): Valores de entrada / features.
        """

        #Inicia uma lista para armazenar as predições
        predict = []
        PREFIX = "Layer-"
        #--------------------------INICIALIZANDO O PREDIÇÃO------------------------------
        #Percorre feature por feature
        for i in range(len(x)):

            layer_active = x[i]
            
            for id_layer in range(self._n_layers):
                layer = np.dot(layer_active, self._layers[PREFIX + str(id_layer)])
                layer_active = self.sigmoid(layer)

            #Predição
            predict.append([self.thresh(layer_active)])

        return predict

    def initialize_weights(self, x, neurons, n_layers):
        """
        Info:
            Esta função inicializa os pesos das camadas da rede neural.

        Params:
            x: Features de entrada da rede.
            neurons: Quantidade de neurônios definidos para a camada oculta.
        """

        PREFIX = "Layer-"

        #Percorre o numero de caracteristicas
        generated_weights = []
        #Camada de entrada
        for _ in range(len(x[0])):

            #Gera uma lista de valores aleatorios
            generated_weights.append([round(random.uniform(-1, 1), 3) for _ in range(neurons)])
        
        self._layers[PREFIX+'0'] = np.asarray(generated_weights)

        #Camada oculta
        for layer in range(1, n_layers-1):
            self._weights_layer2 = []

            for _ in range(neurons):
                generated_weights = [round(random.uniform(-1, 1), 3) for _ in range(neurons)]
                self._weights_layer2.append(generated_weights)

            self._layers[PREFIX + str(layer)] = np.asarray(self._weights_layer2)

        #Camada de saida
        self._weights_layer2 = []
        for _ in range(neurons):
            generated_weights = [round(random.uniform(-1, 1), 3)]
            self._weights_layer2.append(generated_weights)

        self._layers[PREFIX + str(n_layers-1)] = np.asarray(self._weights_layer2)
        

    
    def sigmoid(self, value):
        """
        Info:
            Função para aplicar a função sigmoid.
        Params:
            value (float): Valor para aplicar a função.
        """
        return 1 / (1 + np.exp(-value))
    
    def sigmoid_derivative(self, value):
        """
        Info:
            Função para aplicar a derivada da função sigmoid.
        Params:
            value (float): Valor para aplicar a derivada.
        """
        return value * (1 - value)

    def thresh(self, value):
        """
        Info:
            Função para aplicar a função de threshold.
        Params:
            value (float): Valor para aplicar a função.
        """
        return 1 if value >= 0.5 else 0

    def check_params(self, epoch, neurons, n_layers, learning_rate):
        """
        Info:
            Função para verificar os parâmetros de entrada.
        Params:
            epoch (int): Número de épocas.
            neurons (int): Número de neurônios.
            n_layers (int): Número de camadas.
            learning_rate (float): Taxa de aprendizado.
        """
        if epoch < 1:
            raise ValueError("O número de épocas deve ser maior que 0.")
        if neurons < 1:
            raise ValueError("O número de neurônios deve ser maior que 0.")
        if n_layers < 2:
            raise ValueError("O número de camadas deve ser maior que 1.")
        if learning_rate <= 0:
            raise ValueError("A taxa de aprendizado deve ser maior que 0.")
