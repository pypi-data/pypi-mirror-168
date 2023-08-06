from cmath import tanh
import numpy as np
import matplotlib.pyplot as plt

sigmoid = lambda x: 1/(1 + np.e**-x)
tanh = lambda x: np.tanh(x)
relu = lambda x: np.maximum(0, x)

def randoms_points(n = 100):
    x = np.random.uniform(0.0, 1.0, n)
    y = np.random.uniform(0.0, 1.0, n)

    return np.array([x, y]).T

class Perceptron:
    def __init__(self, n_inputs, act_f):
        self.weights = np.random.rand(n_inputs, 1)
        self.bias = np.random.rand()
        self.act_f = act_f
        self.n_inputs = n_inputs

    def predict(self, x):
        return self.act_f(x @ self.weights + self.bias)

    def fit(self, x, y, epochs = 100):

        for i in range(epochs):
            for j in range(self.n_inputs):
                output = self.predict(x[j])
                error = y[i] - output
                self.weights = self.weights + (error*x[j][1])
                self.bias = self.bias + error
def main():
    points = randoms_points(10000)
    #plt.scatter(points[:,0],points[:,1], s = 10)
    #plt.show()
    x = np.array([
        [0,0],
        [0,1],
        [1,0],
        [1,1]
    ])

    y = np.array([
        [0],
        [1],
        [1],
        [1]
    ])

    p_or = Perceptron(2,sigmoid)

    yp = p_or.predict(points)
    plt.scatter(points[:,0], points[:,1],s = 10, c = yp, cmap = 'GnBu')
    plt.show()

if __name__ == '__main__':
    main()
