import Gnuplot

def plotData(title, xlabel, ylabel, args):
    """
    args is a list of file names containing relevant data
    """

    g = Gnuplot.Gnuplot()
    g.title(title)
    g.xlabel(xlabel)
    g.ylabel(ylabel)
    g('set term png')
    g('set out "plots/{}.png"'.format(title))
    data = Gnuplot.Data(*args)
    g.plot(data)
    