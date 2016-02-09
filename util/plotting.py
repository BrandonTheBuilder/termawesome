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


def plotComponent(name, data, int_p):
    # Exergetic Efficiency
    ef = [c.ef for c in data]
    plotData('Exergetic Efficiency of {}'.format(name), 'Intermediate Pressure (kPa)',
        'Exergetic Efficiency', [int_p, ef])
    work = [c.w for c in data]
    yf_in = [c.yf_in for c in data]
    yf_out = [c.yf_out for c in data]
    ex_destroyed = [c.exergyDestroyed for c in data]
    plot_work = Gnuplot.Data(int_p, work, title='Exergy lost to work', with_='lines')
    plot_yf_in = Gnuplot.Data(int_p, yf_in, title='Sum of Exergy Flow in', with_='lines')
    plot_yf_out = Gnuplot.Data(int_p, yf_out, title='Sum of Exergy Flow out', with_='lines')
    plot_ex_destroyed = Gnuplot.Data(int_p, ex_destroyed, title='Exergy Destroyed', with_='lines')
    g = Gnuplot.Gnuplot()
    g.title('Exergy Balance for {}'.format(name))
    g.ylabel('kJ/kg')
    g.xlabel('Intermediate Pressure (kPa)')
    g('set term png')
    g('set out "plots/{}.png"'.format(name))
    g.plot(plot_work, plot_yf_in, plot_yf_out, plot_ex_destroyed)

    