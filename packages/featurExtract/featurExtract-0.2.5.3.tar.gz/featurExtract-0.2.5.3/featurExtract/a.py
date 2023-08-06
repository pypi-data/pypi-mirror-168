import matplotlib.pyplot as plt 

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
ax.plot([1,2],[2,2],solid_capstyle='butt', linewidth=0.7,color='grey')
ax.plot([2,6],[2,2],solid_capstyle='butt', linewidth=3,color='grey')
plt.arrow(0.1,0.1,0.5,0.3)
plt.show()
