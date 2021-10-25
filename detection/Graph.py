import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        pass

    def graph_x_against_y(self, x, y, x_label="X", y_label="Y", title="Graph"):
        # plotting the points
        plt.plot(x, y)
        plt.scatter(x, y)

        x_spine = [x[0], x[len(x) - 1]]
        y_spine = [y[0], y[len(y) - 1]]

        plt.plot(x_spine, y_spine, label="spine")

        # naming the x axis
        plt.xlabel(x_label)
        # naming the y axis
        plt.ylabel(y_label)

        # giving a title to my graph
        plt.title(title)

        # function to show the plot
        plt.show()