from skimage.feature import graycomatrix, graycoprops
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from skimage.io import imread
import numpy as np

class Features:

    @staticmethod
    def GLCM(dataset, steps = 1):
        """
        Info:
            Calcula a matriz de Co-ocorrencia de níveis de cinza de um dataset.
        Params:
            dataset (array numpy, array, imread_collection): Dataset de imagens.
            steps (array): Lista de deslocamentos de distância de pares de pixels.
        Return:
            Matriz isotrópica.
        """
        matrix = []

        for img in dataset:
            matrix0 = graycomatrix(img, [steps], [0], normed=True)
            matrix1 = graycomatrix(img, [steps], [np.pi/4], normed=True)
            matrix2 = graycomatrix(img, [steps], [np.pi/2], normed=True)
            matrix3 = graycomatrix(img, [steps], [3*np.pi/4], normed=True)
            matrix.append((matrix0+matrix1+matrix2+matrix3)/4)
        
        return np.asarray(matrix)
    
    @staticmethod
    def GLCM_props(matrix):
        """
        Info:
            Calcula as propriedades da matriz de Co-ocorrencia de níveis de cinza.
        Params:
            matrix (array): Array de matrizes de Co-ocorrencia de níveis de cinza.
        Return:
            Matriz com as propriedades de contraste, dissimilaridade, homogeneidade, 
            energia, correlação e ASM.
        """
        props = []

        for mat in matrix:
            prop = np.zeros((6))
            prop[0] = graycoprops(mat,'contrast')
            prop[1] = graycoprops(mat,'dissimilarity')
            prop[2] = graycoprops(mat,'homogeneity')
            prop[3] = graycoprops(mat,'energy')
            prop[4] = graycoprops(mat,'correlation')
            prop[5] = graycoprops(mat,'ASM')
            props.append(prop)
        
        return np.asarray(props)

    @staticmethod
    def categorize(dataset, new_value_bit, old_value_bit):
        """
        Info:
            Categoriza os bits de imagens de um dataset.
        Params:
            dataset (array numpy): Dataset de imagens bi-dimensionais.
            new_value_bit (int): Novo valor de bits.
            old_value_bit (int): Valor dos bits da imagem
        Return:
            Array com as imagens categorizadas.
        """
        categorized = []

        for img in dataset:

            #Guardando as dimensões da imagem original.
            Lines,Columns = img.shape;

            img = np.array(img, dtype=np.float64)

            #Categorizando os bits.
            for line in range(Lines):
                for Colum in range(Columns):
                    img[line, Colum] = (((2**new_value_bit)-1) * img[line, Colum]) // ((2**old_value_bit)-1)

            img = np.array(img, dtype=np.uint8)

            categorized.append(img)

        return np.asarray(categorized)
    @staticmethod
    def PCA(X, n_components):
        """
        Info:
            Aplica o algoritmo de redução de dimensionalidade PCA em uma matriz de características.
        Params:
            X (array): Matriz de características.
            n_components (int): Número de componentes principais.
        Return:
            Matriz de características reduzida.
        """
        
        X = StandardScaler().fit_transform(X)

        pca = PCA(n_components=n_components)
        components = pca.fit_transform(X)
        
        return components