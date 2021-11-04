import matplotlib.pyplot as plt

f, ax = plt.subplots(1)

x_data = [5, 7, 4, 20, 21, 19, 10, 13, 12, 11, 17, 18, 17]
y_data = [6, 5, 5, 30, 29, 28, 25, 24, 20, 23, 4, 5, 6]

data = []

for index in range(len(x_data)):
    data.append([x_data[index], y_data[index]])

print(data)

ax.scatter(x_data, y_data)
ax.set_ylim(bottom=0)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Example Clusters')
plt.show()

