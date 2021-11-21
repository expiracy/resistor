import matplotlib.pyplot as plt


# A helper class that allows data to be visualised.
class Graph:
    def __init__(self):
        pass

    # Plots the spine graph.
    def graph_x_against_y(self, x, y, x_label="X", y_label="Y", title="Graph"):
        plt.plot(x, y)
        plt.scatter(x, y)

        # x_spine = [x[0], x[len(x) - 1]]
        # y_spine = [y[0], y[len(y) - 1]]

        # plt.plot(x_spine, y_spine, label="spine")

        plt.xlabel(x_label)

        plt.ylabel(y_label)

        plt.title(title)

        plt.show()
