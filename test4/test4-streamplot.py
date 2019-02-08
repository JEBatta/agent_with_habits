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

Y, X = np.mgrid[0.02:0.98:48j, 0.02:0.98:48j]
U, V = np.mgrid[0.0:0.0:48j, 0.0:0.0:48j]

#with open('test4_influence_after_training.csv','rb') as f:
with open('test4_influence_after_control.csv','rb') as f:
 reader = csv.reader(f)
 next(reader)	
 i = 0
 for	 row in reader:
  U[i/48][i%48], V[i/48][i%48] = float(row[2]),float(row[3])
  #df[i/31][i%31] = float(row[4]) 
  #U[i%31][i/31],V[i%31][i/31] = float(row[3]),float(row[2])
  i += 1
speed = np.sqrt(U*U + V*V)
fig = plt.figure(figsize=(5, 5))
gs = gridspec.GridSpec(nrows=1, ncols=1, height_ratios=[1])

#  Varying line width along a streamline
ax2 = fig.add_subplot(gs[0, 0])
lw = speed / speed.max()	
print(speed.max())
print(speed.min())
ax2.streamplot(X, Y, U, V, density=0.7, color='k', linewidth=lw)
#ax2.set_title('Influence of medium after training \n (t=20)')
ax2.set_title('Influence of medium after control \n (t=200)')

plt.tight_layout()
#plt.savefig("test4_training.png")
plt.savefig("test4_control.png")
plt.show()
