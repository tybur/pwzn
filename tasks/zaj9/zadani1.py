%%px

import numpy as np
from matplotlib import pylab
from scipy.optimize import curve_fit


def func(x, a, b, c, d, f):
    return a * np.exp(-((x-b)*(x-b))/(2*c*c)) + d + f*x


def get_init_params(fdata):
    xdata = np.linspace(-40, 40, 10000)
    '''
    a = np.max(fdata)
    b = np.average(xdata * fdata)
    c = np.sqrt(np.average((xdata-b)*(xdata-b)*fdata))
    d = f = 0
    '''
    d = np.average(fdata)
    ydata = fdata - np.min(fdata)
    s = np.sum(ydata)
    a = np.max(ydata)
    b = np.sum(xdata * ydata)/s
    c = np.sqrt(np.sum((xdata-b)*(xdata-b)*ydata)/s)
    f = np.median((fdata[1:]-fdata[:-1])/(8/1000))
    return a,b,c,d,f


def fit_func(fdata):
    xdata = np.linspace(-40, 40, 10000)
    #initial guesses for parameters:
    f = np.median((fdata[1:]-fdata[:-1])/(8/1000))
    d = fdata[0] - (-40)*f
    ydata = fdata - (f*xdata+d)     #detrended data
    ydata[ydata < 0] = 0
    s = np.sum(ydata)
    a = np.max(ydata)
    b = np.sum(xdata * ydata)/s
    c = np.sqrt(np.sum((xdata-b)*(xdata-b)*ydata)/s)
    try:
        popt, pconv = curve_fit(func, xdata, fdata, [a,b,c,d,f])
    except Exception as e:
        return None
    return popt, pconv


def get_results(dm):
    results = []
    for data in dm:
        results.append(fit_func(data))
    return results



m = np.memmap("/home/tybur/PWZN/data/zaj9/data.bin", dtype="float", shape=(1000, 10000))

index = 16
res = fit_func(m[index])
print(res[0])
print(res[1])
xdata = np.linspace(-40, 40, 10000)
pylab.plot(func(xdata, *res[0]))
pylab.plot(m[index])
pylab.show()


def output_diff(m, out_filename)
    sres = []
    outfile = open(out_filename, 'w')
    xdata = np.linspace(-40,40,10000)
    for i in range(1000):
        r = fit_func(m[i])
        if r:
            fitted = func(xdata, *fit_func(m[i])[0])
            diff = np.average(np.abs(m[i] - fitted))
            outfile.write('%d %f\n' % (i, diff))
        else:
            outfile.write('%d None\n' % i)
        print("%d done" % i)
    outfile.close()



def show_fit_result(m, index):
    res = fit_func(m[index])
    #print(res[0])
    #print(res[1])
    xdata = np.linspace(-40, 40, 10000)
    plt.plot(xdata, func(xdata, *res[0]))
    plt.plot(xdata, m[index])
    plt.show()


def show_f(m, index):
    plt.plot(m[index])
    plt.show()
