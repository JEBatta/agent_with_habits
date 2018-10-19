"""
==========
Streamplot
==========

A stream plot, or streamline plot, is used to display 2D vector fields. This
example shows a few features of the :meth:`~.axes.Axes.streamplot` function:
    * Varying the line width along a streamline.

This code is a modification from: 
https://matplotlib.org/gallery/images_contours_and_fields/plot_streamplot.html

"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import csv

Y, X = np.mgrid[0.0:1.0:101j, 0.0:1.0:101j]
m1, m2 = np.mgrid[0.0:0.0:101j, 0.0:0.0:101j]
v1, v2 = np.mgrid[0.0:0.0:101j, 0.0:0.0:101j]
a1, a2 = np.mgrid[0.0:0.0:101j, 0.0:0.0:101j]

with open('influence_frozen_at_20.csv','rb') as f:
 reader = csv.reader(f)
 next(reader)
 i = 0
 for row in reader:
  m1[i/100][i%100],m2[i/100][i%100] = float(row[2]),float(row[3])
  v1[i/100][i%100],v2[i/100][i%100] = float(row[4]),float(row[5])
  a1[i/100][i%100],a2[i/100][i%100] = float(row[6]),float(row[7])
  i += 1
speed = np.sqrt(m1*m1 + m2*m2)

fig = plt.figure(figsize=(12, 4))
gs = gridspec.GridSpec(nrows=1, ncols=3, height_ratios=[1])

#  Varying line width along a streamline
ax2 = fig.add_subplot(gs[0, 0])
lw = speed / speed.max()
ax2.streamplot(X, Y, v1, v2, density=0.7, color='k', linewidth=lw)
ax2.set_title('Velocity')

ax2 = fig.add_subplot(gs[0, 1])
lw = speed / speed.max()
ax2.streamplot(X, Y, a1, a2, density=0.7, color='k', linewidth=lw)
ax2.set_title('Attraction')

ax2 = fig.add_subplot(gs[0, 2])
lw = speed / speed.max()
ax2.streamplot(X, Y, m1, m2, density=0.7, color='k', linewidth=lw)
ax2.set_title('Combined')

plt.tight_layout()
plt.show()
