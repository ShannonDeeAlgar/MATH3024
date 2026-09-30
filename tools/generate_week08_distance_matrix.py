"""Small exact example linking pair distances to percolation connectivity."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from figure_style import apply_course_figure_style

apply_course_figure_style()
out = Path(__file__).resolve().parents[1] / 'notebooks/week08/images'
x = np.arange(6)
names = list('ABCDEF')
labels = np.array([1, 1, 0, 2, 2, 2])
distance = np.abs(x[:, None] - x[None, :])
r = 2
within = (distance > 0) & (distance <= r)
shell = distance == r
connected = (labels[:, None] == labels[None, :]) & (labels[:, None] > 0)
upper = np.triu(np.ones((6, 6), dtype=bool), 1)
assert np.count_nonzero(within & upper) == 9
assert np.count_nonzero(shell & upper) == 4
assert np.count_nonzero(shell & connected & upper) == 1

fig = plt.figure(figsize=(11.5, 6.3), layout='constrained')
gs = fig.add_gridspec(2, 2, height_ratios=[1, 4])
sites = fig.add_subplot(gs[0, :])
sites.set(xlim=(-.6, 5.6), ylim=(-.6, .65))
sites.axis('off')
for i, name in enumerate(names):
    colour = ['#BFC5CD', '#3C78A8', '#D95F3D'][labels[i]]
    sites.scatter(i, 0, s=600, marker='s', facecolor=colour, edgecolor='#172A50')
    sites.text(i, .32, name, ha='center', fontsize=14)
    sites.text(i, -.38, f'x = {i}', ha='center', fontsize=13)
sites.set_title('Site colours show connectivity, not distance\nBlue: open cluster A–B; orange: open cluster D–F; grey: blocked C', fontsize=13)
axes = [fig.add_subplot(gs[1, i]) for i in range(2)]
im = axes[0].imshow(distance, cmap='Greys', vmin=0, vmax=5)
axes[0].set_title(r'Distance matrix: $d_{ij}=|x_i-x_j|$', fontsize=16)
fig.colorbar(im, ax=axes[0], shrink=.8, label='Distance (lattice spacings)')
axes[1].imshow(within, cmap=ListedColormap(['#F3F6FA', '#209582']), vmin=0, vmax=1)
axes[1].set_title(r'Thresholded: $0<d_{ij}\leq2$', fontsize=16)
for ax in axes:
    ax.set_xticks(x, names)
    ax.set_yticks(x, names)
    ax.set_xlabel('Site j')
    ax.set_ylabel('Site i')
    for spine in ax.spines.values():
        spine.set_visible(False)
for i in x:
    for j in x:
        axes[0].text(j, i, str(distance[i,j]), ha='center', va='center',
                     color='white' if distance[i,j]>=3 else '#172A50', fontsize=13)
        axes[1].text(j, i, '—' if i==j else str(int(within[i,j])),
                     ha='center', va='center', color='white' if within[i,j] else '#172A50', fontsize=13)
for suffix in ['svg', 'png']:
    fig.savefig(out / f'percolation_distance_matrix.{suffix}', dpi=160)
plt.close(fig)
print('Verified: 9 pairs within r=2; 4 at r=2; 1 connected pair at r=2.')
