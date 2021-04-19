import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle

# no. states explore
y_order = [
    [15, 35, 42, 59, 127],
    [14, 23, 24, 41, 77],
    [80, 627, 621, 1358, 10846]
]

y_reverse = [
    [13, 35, 42, 59, 127],
    [11, 29, 46, 82, 92],
    [81, 832, 862, 2172, 11274]
]

x = [2, 3, 4, 5, 6]

m = MarkerStyle("x")

# for y in y_order:
#     plt.plot(x, y)
#     m._transform.rotate_deg(45)
#     plt.scatter(x, y, marker=m)
# plt.xlabel('square grid length')
# plt.ylabel('no. of states explored')
# plt.xticks(x)
# plt.title('No, of states explored VS square grid length (Down, Up, Right, Left)')
# plt.legend(['bfs', 'dfs', 'dfid'])
# plt.savefig('fig_order.png')


for y in y_reverse:
    plt.plot(x, y)
    m._transform.rotate_deg(45)
    plt.scatter(x, y, marker=m)
plt.xlabel('square grid length')
plt.xticks(x)

plt.ylabel('no. of states explored')
plt.title('No, of states explored VS square grid length (Left, Right, Up, Down)')
plt.legend(['bfs', 'dfs', 'dfid'])
plt.savefig('fig_rev.png')
