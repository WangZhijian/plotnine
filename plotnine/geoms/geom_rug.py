import numpy as np
import matplotlib.collections as mcoll

from ..utils import to_rgba, make_line_segments, SIZE_FACTOR
from ..doctools import document
from .geom import geom


@document
class geom_rug(geom):
    """
    Marginal rug plot

    {usage}

    Parameters
    ----------
    {common_parameters}
    sides : str (default: bl)
        Sides onto which to draw the marks. Any combination
        chosen from the characters ``btlr``, for *bottom*, *top*,
        *left* or *right* side marks.
    """
    DEFAULT_AES = {'alpha': 1, 'color': 'black', 'size': 0.5,
                   'linetype': 'solid'}
    DEFAULT_PARAMS = {'stat': 'identity', 'position': 'identity',
                      'na_rm': False, 'sides': 'bl'}
    legend_geom = 'path'

    @staticmethod
    def draw_group(data, panel_params, coord, ax, **params):
        data = coord.transform(data, panel_params)
        data['size'] *= SIZE_FACTOR

        has_x = 'x' in data.columns
        has_y = 'y' in data.columns

        if has_x or has_y:
            n = len(data)
        else:
            return

        rugs = []
        sides = params['sides']
        xmin, xmax = panel_params['x_range']
        ymin, ymax = panel_params['y_range']
        xheight = (xmax-xmin)*0.03
        yheight = (ymax-ymin)*0.03

        if has_x:
            if 'b' in sides:
                x = np.repeat(data['x'].values, 2)
                y = np.tile([ymin, ymin+yheight], n)
                rugs.extend(make_line_segments(x, y, ispath=False))

            if 't' in sides:
                x = np.repeat(data['x'].values, 2)
                y = np.tile([ymax-yheight, ymax], n)
                rugs.extend(make_line_segments(x, y, ispath=False))

        if has_y:
            if 'l' in sides:
                x = np.tile([xmin, xmin+xheight], n)
                y = np.repeat(data['y'].values, 2)
                rugs.extend(make_line_segments(x, y, ispath=False))

            if 'r' in sides:
                x = np.tile([xmax-xheight, xmax], n)
                y = np.repeat(data['y'].values, 2)
                rugs.extend(make_line_segments(x, y, ispath=False))

        color = to_rgba(data['color'], data['alpha'])
        coll = mcoll.LineCollection(rugs,
                                    edgecolor=color,
                                    linewidth=data['size'],
                                    linestyle=data['linetype'],
                                    zorder=params['zorder'])
        ax.add_collection(coll)
