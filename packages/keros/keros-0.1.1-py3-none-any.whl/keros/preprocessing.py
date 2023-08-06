import numpy as np
from skimage.color import rgb2gray

class Preprocessing:

    @staticmethod
    def normalize(dataset):
        """
        Info:
            Normaliza os valores de um dataset.
        Params:
            dataset (array numpy): Dataset com imagens 2D-dimensional.
        Return:
            Dataset normalizado.
        """
        normalized = []

        for img in dataset:
            normalized.append((img - np.min(img)) / (np.max(img) - np.min(img)))

        return np.asarray(normalized)

    @staticmethod
    def label_encoder(names, class_1, class_2):
        """
        Info:
            Codifica os valores de um dataset entre 0 e 1.
        Params:
            dataset (array numpy): Dataset com o nome das classes de cada imagem.
        Return:
            Dataset codificado.
        """
        encoded = []

        for name in names:
        
            if name.lower() == class_1.lower():
                encoded.append([1])

            elif name.lower() == class_2.lower():
                encoded.append([0])

        return np.asarray(encoded)

    @staticmethod
    def to_gray(dataset):
        """
        Info:
            Converte um dataset de imagens RGB para escala de cinza.
        Params:
            dataset (array numpy): Dataset com imagens 3D-dimensional.
        Return:
            Dataset convertido.
        """
        gray = []

        for img in dataset:
            gray.append(rgb2gray(img))

        return np.asarray(gray)

    def convert_to_integer(dataset):
        """
        Info:
            Converte um dataset de imagens float para int entre 0 e 255.
        Params:
            dataset (array numpy): Dataset com imagens 2D-dimensional.
        Return:
            Dataset convertido.
        """
        integer = []

        for img in dataset:
            integer.append((img*255).astype(np.uint8))

        return np.asarray(integer)
