import numpy as np
import matplotlib.pyplot as plt


def half_violin_plot(ax, *args, show_positive=True, color='red', **kwargs):
    v = ax.violinplot(*args, **kwargs)

    coord_idx = int(not kwargs.get('vert', True))
    for b in v['bodies']:
        coords = b.get_paths()[0].vertices[:, coord_idx]
        # get the center
        m = np.mean(coords)
        # modify the paths to not go further right than the center
        clip_limits = (m, +np.inf) if show_positive else (-np.inf, m)
        b.get_paths()[0].vertices[:, coord_idx] = np.clip(coords, *clip_limits)
        b.set_color(color)
        b.set_edgecolor('dimgrey')
        b.set_linestyle('-')
        b.set_linewidth(1)
        b.set_alpha(1)
    return v

def strip_plot(ax, data, pos, vert=True, jitter=0.01, **kwargs):
    yvals = np.array(data)
    xvals = np.full_like(data, pos) + np.random.randn(len(yvals)) * jitter
    if not vert:
        xvals, yvals = yvals, xvals
    ax.scatter(xvals, yvals, **kwargs)
    return np.array([xvals, yvals]).transpose()

def raincloud_plot(ax, data, pos=0., vert=True, show_positive=False, jitter=0.01, bw='scott', width=0.5, raindrop_size=10, color='tab:blue'):
    half_violin_plot(ax, data, showextrema=False, bw_method=bw, positions=[pos], color=color, vert=vert, show_positive=show_positive, widths=width)
    
    umbrella_offset = (-1 if show_positive else +1) * 15 * jitter
    umbrella_pos = pos + umbrella_offset
    raindrops_pos = strip_plot(ax, data, umbrella_pos, vert, jitter, s=raindrop_size, color=color)
    
    umbrella_linewidth = 1.5
    umbrella_color = 'dimgrey'
    ax.boxplot(data, whis=(5,95), showfliers=False, positions=[umbrella_pos], widths=width/8,
               medianprops={'color':umbrella_color},
               boxprops={'linewidth':umbrella_linewidth, 'color':umbrella_color},
               whiskerprops={'linewidth':umbrella_linewidth, 'color':umbrella_color},
               capprops={'linewidth':umbrella_linewidth, 'color':umbrella_color})
    
    return umbrella_pos, raindrops_pos

def draw_line_between_point_pair(ax, point1, point2, **kwargs):
    ax.plot([point1[0], point2[0]], [point1[1], point2[1]], **kwargs)

def paired_raincloud_plot(ax, data1, data2, positions=[0., 1], labels=None, **kwargs):
    def draw_lightning(ax, raindrops1_pos, raindrops2_pos):
        for drop1, drop2 in zip(raindrops1_pos, raindrops2_pos):
            draw_line_between_point_pair(ax, drop1, drop2, color='black', alpha=0.1)
        
    umbrella1_pos, raindrops1_pos = raincloud_plot(ax, data1, pos=positions[0], show_positive=False, **kwargs)
    umbrella2_pos, raindrops2_pos = raincloud_plot(ax, data2, pos=positions[1], show_positive=True, **kwargs)
    
    draw_lightning(ax, raindrops1_pos, raindrops2_pos)
        
    if labels is not None:
        ax.set_xticks([umbrella1_pos, umbrella2_pos], labels)
