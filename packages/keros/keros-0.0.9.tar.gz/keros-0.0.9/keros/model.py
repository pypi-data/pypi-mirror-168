import random
import numpy as np
from .model_tools import Tools
#Primeira versão estável do modelo.
#Possui apenas a camada de entrada, um camada oculta e a camada de saida.


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
        self._weights_layer1 = []
        self._weights_layer2 = []
        #Inicializa uma variável para armazenar o erro.
        self._mean_absolute_loss = 0
        #Metrics
        self._accuracy = 0
        self._precision = 0
        self._recall = 0
        self._f1 = 0
        self._kappa = 0

    def metrics(self):
        """
        Info:
            Retorna as métricas da rede neural.
        """
        return self._accuracy, self._precision, self._recall, self._f1, self._kappa

    def fit(self, x, y, epoch=5, neurons=5, learning_rate=0.0001, error_threshold=0.1, moment=1):
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
            learning_rate (float): Taxa de aprendizagem da rede.
            error_threshold (float): Valor máximo para o loss.
            moment (float): Otimiza o aprendizado evitantando mínimos locais na curva de erro.
        """
        #--------------------------INICIALIZANDO OS PESOS------------------------------
        self.initialize_weights(x, neurons)

        #--------------------------INICIALIZANDO O TREINO------------------------------
        for epc in range(epoch):
            layer1 = np.dot(x, self._weights_layer1)
            layer1_active = self.sigmoid(layer1)

            layer2 = np.dot(layer1_active, self._weights_layer2)
            layer2_active = self.sigmoid(layer2)

            #------------------------CALCULANDO O ERRO---------------------------------
            loss = y - layer2_active
            self._mean_absolute_loss = np.mean(np.abs(loss))
            print("Loss: {}".format(self._mean_absolute_loss))

            if self._mean_absolute_loss <= error_threshold:
                y_pred = [[self.thresh(i)] for i in layer2_active]
                self._accuracy, self._precision, self._recall, self._f1, self._kappa = Tools.metrics(y, y_pred)
                break
            
            #---------------------CALCULANDO O GRADIENTE-------------------------------
            #Layer 2
            derivative_layer2 = self.sigmoid_derivative(layer2_active)
            delta_layer2 = loss * derivative_layer2

            #Layer 1
            weights_layer2_transpose = self._weights_layer2.T
            delta_layer2XWeights_layer2_transpose = delta_layer2.dot(weights_layer2_transpose)
            delta_layer1 = delta_layer2XWeights_layer2_transpose * self.sigmoid_derivative(layer1_active)

            #---------------------ATUALIZANDO OS PESOS-----------------------------------
            #Layer 2
            layer1_transpose = layer1_active.T
            weights_layer2Xdelta_layer2 = layer1_transpose.dot(delta_layer2)
            self._weights_layer2 = (self._weights_layer2 * moment) + (weights_layer2Xdelta_layer2 * learning_rate)

            #Layer 1
            x_transpose = x.T
            xXDelta_layer1 = x_transpose.dot(delta_layer1)
            self._weights_layer1 = (self._weights_layer1 * moment) + (xXDelta_layer1 * learning_rate)

        #-------------------------FIM DO TREINO-------------------------------------------

        #---------------------CALCULANDO MÉTRICAS-----------------------------------------
        y_pred = [[self.thresh(i)] for i in layer2_active]
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

        #--------------------------INICIALIZANDO O PREDIÇÃO------------------------------
        #Percorre feature por feature
        for i in range(len(x)):
            #Layer 1
            layer1 = np.dot(x[i], self._weights_layer1)
            layer1_active = self.sigmoid(layer1)

            #Layer 2
            layer2 = np.dot(layer1_active, self._weights_layer2)
            layer2_active = self.sigmoid(layer2)

            #Predição
            predict.append([self.thresh(layer2_active)])

        return predict

    def initialize_weights(self, x, neurons):
        """
        Info:
            Esta função inicializa os pesos das camadas da rede neural.

        Params:
            x: Features de entrada da rede.
            neurons: Quantidade de neurônios definidos para a camada oculta.
        """
        #Percorre o numero de caracteristicas
        for _ in range(len(x[0])):

            #Gera uma lista de valores aleatorios
            generated_weights = [round(random.uniform(-1, 1), 3) for _ in range(neurons)]

            #Junta os valores aleatorios para formarem os pesos da camada 0
            self._weights_layer1.append(generated_weights)

        #Percorre o numero de neuronios
        for _ in range(neurons):

            #Gera uma lista de valores aleatorios
            generated_weights = [round(random.uniform(-1, 1), 3)]

            #Junta os valores aleatorios para formarem os pesos da camada 1
            self._weights_layer2.append(generated_weights)

        #Converte a lista em array numpy
        self._weights_layer1 = np.asarray(self._weights_layer1)
        self._weights_layer2 = np.asarray(self._weights_layer2)
    
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

    