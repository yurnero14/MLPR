import numpy
import matplotlib
import matplotlib.pyplot as plt
import scipy.stats
def mcol(v):
    return v.reshape((v.size, 1))

def empirical_mean(X):
    return mcol(X.mean(1))

def empirical_covariance(X):
    mu = empirical_mean(X)
    DC = X - mu.reshape((mu.size, 1))
    C = numpy.dot(DC, DC.T)/ float(DC.shape[1])

    return C

def empirical_withinclass_cov(D, labels):
    SW = 0
    for i in set(list(labels)):
        X = D[:, labels == i]
        SW += X.shape[1] * empirical_covariance(X)
    return SW / D.shape[1]


def empirical_betweenclass_cov(D, labels):
    SB = 0
    muGlob = empirical_mean(D)  # mean of the dataset
    for i in set(list(labels)):
        X = D[:, labels == i]
        mu = empirical_mean(X)  # mean of the class
        SB += X.shape[1] * numpy.dot((mu - muGlob), (mu - muGlob).T)
    return SB / D.shape[1]
def load(fname):
    DList = []
    labelsList = []
    hLabels = {
        'Iris-setosa': 0,
        'Iris-versicolor': 1,
        'Iris-virginica': 2
    }
    #efficient way since not a lot of labels and we can just compare and create a list of labels and hence a vector
    with open(fname) as f:
        for line in f:
            try:
                attrs = line.split(',')[0:4]
                attrs = mcol(numpy.array([float(i) for i in attrs]))
                name = line.split(',')[-1].strip()
                label = hLabels[name]
                DList.append(attrs)
                labelsList.append(label)
            except:
                pass
    D = numpy.hstack(DList)
    L = numpy.array(labelsList, dtype=numpy.int32)
    return D, L

def PCA_red(D, m):

    mu = D.mean(1)
    DC = D - mu.reshape((mu.size,1))

    C = numpy.dot(DC, DC.T)/ float(DC.shape[1])
    s, U = numpy.linalg.eigh(C)

    P = U[:, ::-1][:, 0:m]

    PCA_D = numpy.dot(P.T, D)
    print("The mean is: ", mu)
    print("the covar matrix is: ", C)
    return PCA_D, P

def LDA(D, L, m):
    SW = empirical_withinclass_cov(D, L)
    SB = empirical_betweenclass_cov(D, L)
    print("the within: ", SW)
    print("the between: ", SB)
    s, U = scipy.linalg.eigh(SB, SW)
    W = U[:, ::-1][:, 0:m]
    return numpy.dot(W.T, D), W

def plot_scatter(D, L):
    D, _P = PCA_red(D, 7)
    D0 = D[:, L == 0]
    D1 = D[:, L == 1]
    D2 = D[:, L == 2]

    LL, _W = LDA(D, L, 10)
    L0 = LL[:, L == 0]
    L1 = LL[:, L == 1]
    L2 = LL[:, L == 2]
    plt.figure()
    plt.scatter(D0[0, :], D0[1, :], label = 'Setosa')
    plt.scatter(D1[0, :], D1[1, :], label='Versicolor')
    plt.scatter(D2[0, :], D2[1, :], label='Virginica')
    plt.legend()
    plt.figure()
    plt.scatter(L0[0, :], L0[1, :], label='Setosa')
    plt.scatter(L1[0, :], L1[1, :], label='Versicolor')
    plt.scatter(L2[0, :], L2[1, :], label='Virginica')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    # Change default font size - comment to use default values

    D, L = load('iris.csv')

    plot_scatter(D, L)