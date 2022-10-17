import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import time
from LRFutils import progress
from matplotlib.colors import Colormap
from numpy import *

def generate(evolution, monomer, free, stuk, island, occuped_space, save_as = None, plot=False, verbose = False, axis:int=0):

    fig = plt.figure(figsize=(10, 5))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    i=0
    im = ax1.imshow(evolution[0], interpolation='none', aspect='auto', vmin=0, vmax=amax(evolution), cmap="inferno")
    ax2.set_xlim(0, len(evolution))
    ax2.set_ylim(0, max(max(monomer), max(free), max(stuk), max(island)))

    a = progress.Bar(max=len(evolution), prefix="Generating animation")
    def updatefig(i):
        if verbose : print(f"🎞️ Generating animation... Step: {i+1}/{len(evolution)} ({(i+1)/len(evolution)*100:.0f} %)", end="\r")
        im.set_array(evolution[i])
        ax2.plot(i, monomer[i], 'ro', label="Monomers")
        ax2.plot(i, free[i], 'go', label="Free monomers")
        ax2.plot(i, stuk[i], 'bo', label="Stuck monomers")
        ax2.plot(i, occuped_space[i], 'ko', label="Occuped space")
        ax2.plot(i, island[i], 'yo', label="Islands")
        a(i+1)
        return im,
    ani = animation.FuncAnimation(fig, updatefig, range(len(evolution)), blit=True)
    ax2.grid()
    ax2.legend()

    # __________________________________________________
    # Saving animation

    if save_as: 
        if not os.path.isdir(os.path.split(save_as)[0]): os.makedirs(os.path.split(save_as)[0])
        ani.save(save_as)

    if plot: plt.show()

if __name__ == "__main__":
    N = 10
    evolution = zeros((N*N,N,N))
    for i in range(N*N):
        evolution[i, i%N, i//N] = 1

    generate(evolution, save_as="./test.gif", plot=True, axis=-1)

