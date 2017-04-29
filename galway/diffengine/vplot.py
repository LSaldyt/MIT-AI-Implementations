import pandas  as _pd
import seaborn as _sns

def vplot(d):

    d = _pd.DataFrame(d)

    _sns.set()
    _sns.set_style('darkgrid')

    planets = _sns.load_dataset("planets")

    pal = _sns.cubehelix_palette(8, start=.5, rot=-.75, reverse=True)
    _sns.violinplot(data=d, palette=pal, orient='h')

    _sns.plt.show()
