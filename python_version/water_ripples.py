import numpy as np
import sys
from time import sleep
import csv

file_path = 'xyz.csv'

def ripple_xy(previous, current, dampening=0.95):
    '''
        Versiunea clasica, nu sunt sigur ca merge si probabil e slow fiindca python
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
    
    temp = previous
    previous = current
    current = temp

    return previous, current

def init_arrays(width=50, height=50, ripple_intensity=100):
    """
      Returneaza matrici de dimensiunea width*height formata din 0
    de tip np.array si "arunca" o piatra cu intensitatea ripple_intensity
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
        Fara sleep e prea rapid se poate observa efectul :)
   '''
   sleep(0.10)
   print('\x1b[H')
   for i in range(current.shape[0]):
       for j in range(current.shape[1]):
           L = int(abs(current[i, j]) / 31)
           luminance = ' .-:=!*#$'
           print(luminance[L], end='')
       print("\n")


def read_command_line_arguments():
# Implementarea asta de a lua command line arguments nu e prea stralucita 
    if len(sys.argv) != 6:
        sys.exit("\nUsage: water_ripples.py interations width height dampening ripple_intensity\n")
    iterations = int(sys.argv[1])
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    dampening = np.float32(sys.argv[4])
    ripple_intensity = int(sys.argv[5])


def main():
    
    # Implementarea asta de a lua command line arguments nu e prea stralucita 
    if len(sys.argv) != 6:
        sys.exit("\nUsage: water_ripples.py interations width height dampening ripple_intensity show_ripple\n")
    iterations = int(sys.argv[1])
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    dampening = np.float32(sys.argv[4])
    ripple_intensity = int(sys.argv[5])
    show_ripple_bool = int(sys.argv[6])

    # Initializare
    current, previous = init_arrays(width, height, ripple_intensity)
    values = np.zeros((iterations, height, width))
    
    for i in range(iterations):
        previous, current = ripple(previous, current, dampening)
        with open(file_path, 'w') as f:
                
        

        if show_ripple_bool:
            show_ripple(current)

if __name__ == "__main__":
    main()
