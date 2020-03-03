import numpy as np
import matplotlib.pyplot as plt

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
color_index = 0
drawing_list = []


def setup_plot(objects, filename):
    global color_index
    
    plt.axis('equal')
    plt.axis([-10, 110, -10, 110])

    fig = plt.figure()
    ax = plt.subplot(1,1,1)
    t = np.arange(0, 2*np.pi, 0.01)
    
    for shape in objects:
        kind = shape.get_shape()
        
        if kind == 'circle':

            c = shape.get_center()
            r = shape.get_radius()
            x = float(r) * np.sin(t) + float(c[0])
            y = float(r) * np.cos(t) + float(c[1])
            plt.plot(x, y, colors[color_index])
            color_index = (color_index + 1) % len(colors)
            
        elif kind == 'dot':

            c = shape.get_center()
            r = 0.02
            x = float(r) * np.sin(t) + float(c[0])
            y = float(r) * np.cos(t) + float(c[1])
            plt.plot(x, y, colors[color_index])
            color_index = (color_index + 1) % len(colors)
            
        else:

            ax.add_patch(plt.Polygon(shape.get_loop(), fill=None, edgecolor=colors[color_index]))
            color_index = (color_index + 1) % len(colors)
    
    ax.set_xbound(0.0, 100.0)
    ax.set_ybound(0.0, 100.0)
    plt.savefig(filename)
