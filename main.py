from collections import namedtuple
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import axes3d

# Source: https://www.blackjackinfo.com/dealer-outcome-probabilities/#TIDS17
dealer_prob = [[.3536, .3739, .3945, .4164, .4232, .2623, .2447, .2284, .2298, .1665],
			   [.1398, .1350, .1305, .1223, .1654, .3686, .1286, .1200, .1207, .1889],
			   [.1349, .1305, .1259, .1223, .1063, .1378, .3593, .1200, .1207, .1889],
			   [.1297, .1256, .1213, .1177, .1063, .0786, .1286, .3508, .1207, .1889],
			   [.1240, .1203, .1165, .1131, .1017, .0786, .0694, .1200, .3707, .1889],
			   [.1180, .1147, .1112, .1082, .0972, .0741, .0694, .0608, .0374, .0778]]
draw_prob = {"num": 1/13, "face": 3/13, "ace": 1/13}
State = namedtuple('State', ['X', 'Y'])
states = []
for x in range(4,21+1):
	for y in range(2,11+1):
		states.append(State(x, y))

V_curr = defaultdict(int)
V_prev = defaultdict(int)
policy = defaultdict(bool)
epochs = 100
for epoch in range(epochs):
	for state in states:
		# Action = Hit
		hit_value = 0
		for card in range(2,11+1):
			if card < 10:
				p = draw_prob["num"]
			elif card == 10:
				p = draw_prob["face"]
			else:
				p = draw_prob["ace"]

			if state.X + card <= 21:
				hit_value += p * V_prev[State(state.X + card, state.Y)]
			else:
				hit_value += p * (-1)

		# Action = Stick
		p_win = dealer_prob[0][state.Y - 2]
		for i in range(state.X - 17):
			p_win += dealer_prob[i + 1][state.Y - 2]

		if state.X >= 17:
			p_draw = dealer_prob[state.X - 17 + 1][state.Y - 2]
		else:
			p_draw = 0

		p_lose = 1 - p_win - p_draw
		stick_value = 0
		stick_value += p_win * 1  # Win
		stick_value += p_draw * 0  # Draw
		stick_value += p_lose * (-1)  # Lose

		if hit_value > stick_value:
			policy[state] = True
		else:
			policy[state] = False
		V_curr[state] = max(hit_value, stick_value)

	V_prev = V_curr

# Heat Map Plot
plt.figure()
Z = np.zeros([18, 10])
for x in range(4,21+1):
	for y in range(2,11+1):
		Z[x-4, y-2] = policy[State(x, y)]

ax = sns.heatmap(Z, xticklabels=[i for i in range(2,11+1)], yticklabels=[i for i in range(4,21+1)], cmap=sns.color_palette("hls", 2))
ax.invert_yaxis()

# Surface Plot
plt.figure()
Z2 = np.zeros([18, 10])
X = np.array([i for i in range(4,21+1)])
Y = np.array([i for i in range(2,11+1)])
for x in range(4,21+1):
	for y in range(2,11+1):
		Z2[x-4, y-11] = V_curr[State(x, y)]

X, Y = np.meshgrid(Y, X)
ax2 = plt.axes(projection='3d')
ax2.plot_surface(X, Y, Z2, rstride=1, cstride=1, cmap='viridis', edgecolor='none')


plt.show()
