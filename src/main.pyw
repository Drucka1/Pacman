import tkinter as tk
from window import Window
import sys

if __name__ == '__main__':
    root = tk.Tk()
    pacman = Window(root)

    if len(sys.argv) == 3 and sys.argv[1] == '--ai' :
        pacman._toggle_ai(sys.argv[2])
        
        
    pacman.run()


