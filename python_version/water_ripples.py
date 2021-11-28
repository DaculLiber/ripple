import numpy as np
# import pandas as pd
import sys
from time import sleep
import matplotlib.pyplot as plt

def ripple_xy(previous, current, dampening=0.95):
    '''
        Versiunea clasica, nu sunt sigur ca merge bine si probabil e foarte slow
         works great in C++ most likely, dar python e slow
    '''
    for i in range (1, previous.shape[1]-1):
        for j in range(1, previous.shape[0]-1):
            val = ((
                    previous[i-1, j] +
                    previous[i+1, j] +
                    previous[i, j-1] +
                    previous[i, j+1]) / 2 -
                    current[i, j])
            current[i, j] = val * np.float32(dampening)
    
    # Interschimbare
    temp = previous
    previous = current
    current = temp

    return previous, current

def ripple(previous, current, dampening=0.95):
    '''
        Versiunea cu magie de la numpy si vectorizare
    '''
    val = (np.roll(previous, 1, axis=0) + np.roll(previous, -1, axis=0) +
           np.roll(previous, 1, axis=1) + np.roll(previous, -1, axis=1)) / 2 - current
    current = val * dampening
    
    # Interschimbare
    #  am facut interschimbarea aici si nu inauntru la alta functie fiindca referintele la matrici de tip numpy pot fi ciudate :)
    temp = previous
    previous = current
    current = temp

    return previous, current

def init_arrays(width=50, height=50, ripple_intensity=100):
    """
      Returneaza matrici de dimensiunea width*height formata din 0
    de tip np.array si "arunca o piatra" cu intensitatea ripple_intensity in mijlocul lui current
    """
    x = np.zeros((height, width), dtype=np.float32)
    y = np.zeros((height, width), dtype=np.float32)
    height /= 2
    width /= 2
    ripple_intensity = ripple_intensity if ripple_intensity < 255 else 255
    x[int(height), int(width)] = np.float32(ripple_intensity)
    return x, y


def show_ripple(current):
   '''
    Inspirat din donut.c, in functie de valoarea ripple-ului aleg cat de luminat sa fie
     ce arat pe ecran (Still needs some work)
    Fara sleep e prea rapid si nu se poate observa mai nimic :)
   '''
   sleep(0.10)
   print('\x1b[H') # Hieroglifa de clear screen
   for i in range(current.shape[0]):
       for j in range(current.shape[1]):
           L = int(abs(current[i, j]) / 32)
           luminance = ' .-:=!*#$'
           print(luminance[L], end='')
       print("\n")


def main():
    
    # Implementarea asta de a lua command line arguments nu e prea stralucita 
    if len(sys.argv) != 7:
        sys.exit("\nUsage: water_ripples.py iterations width height dampening ripple_intensity show_plot_terminal\n")
    iterations = int(sys.argv[1]) # De cate ori sa faca simularea
    width = int(sys.argv[2]) # Marimiile matricii
    height = int(sys.argv[3])
    dampening = np.float32(sys.argv[4]) # Forta de frecare/reducere
    ripple_intensity = int(sys.argv[5]) # Intensitatea initiala, "cat de tare arunc piatra"
    show_plot_terminal = int(sys.argv[6]) # Daca sa fie varianta terminal sau plot

    # Initializare #
    
    # Initializez curent si previous ca fiind array-uri de 0 de tip numpy.array,
    #  iar in centrul lui current pun intensitatea ripple_intensity
    current, previous = init_arrays(width, height, ripple_intensity)
    # Initializare plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_zlabel('ripple intensity')
    # Creez un meshgrid de tip numpy
    x = range(height)
    y = range(width)
    X, Y = np.meshgrid(x, y)

    # Calculare si afisare #

    # Pentru fiecare iteratie calculez matriciile previous si current,
    #  apoi arat pe plot sau in terminal valorile lui current in functie de X si Y
    for i in range(iterations):
        previous, current = ripple(previous, current, dampening)

        # Daca e 0 arat varianta de plot
        if not show_plot_terminal:
            ax.plot_surface(X, Y, current)
            plt.draw()
            plt.pause(0.05)
            plt.cla()

        # Daca e 1 arat varianta de terminal
        if show_plot_terminal:
            show_ripple(current)    
    
    if not show_plot_terminal:
        plt.show()

if __name__ == "__main__":
    main()
