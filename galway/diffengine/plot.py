import pandas  as _pd
import seaborn as _sns
import matplotlib.pylab as _plt

def vplot(d, filename):
    d = _pd.DataFrame(d)

    _sns.set()
    _sns.set_style('darkgrid')
    pal = _sns.cubehelix_palette(8, start=.5, rot=-.75, reverse=True)
    fig = _sns.violinplot(data=d, palette=pal, orient='h')
    fig = fig.get_figure()
    fig.savefig(filename)

def heatplot(d, filename):
    _plt.xticks(rotation=45)
    _plt.yticks(rotation=0)

    d = _pd.DataFrame(d)

    _sns.set()
    fig = _sns.heatmap(d, linewidths=.5)
    fig = fig.get_figure()
    _plt.tight_layout()
    fig.savefig(filename)
