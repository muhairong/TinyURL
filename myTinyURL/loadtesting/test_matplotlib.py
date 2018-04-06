import matplotlib.pyplot as plt
import numpy
import time


def update_line(l,ax, f,x, y):
    l.set_xdata(numpy.append(l.get_xdata(), x))
    l.set_ydata(numpy.append(l.get_ydata(), y))

    ax.relim()
    ax.autoscale_view()
    f.canvas.draw()
    f.canvas.flush_events()

plt.ion()
'''
figure, ax = plt.subplots()
line1, = ax.plot([], [])
line2, = ax.plot([], [])
ax.set_autoscaley_on(False)
ax.set_xlim(0, 20)
ax.set_ylim(0, 20)
'''
# f1 = plt.figure(1)
f1, ax1 = plt.subplots()
l1, = ax1.plot([], [])
ax1.set_autoscaley_on(True)

f2, ax2 = plt.subplots()
l2, = ax2.plot([], [])
ax2.set_autoscaley_on(True)

for i in range(10):
    update_line(l1, ax1, f1, i, i)
    update_line(l2, ax2, f2, i, i)
    time.sleep(1)