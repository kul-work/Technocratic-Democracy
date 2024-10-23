import sys
import random

from simulation import run_simulation

def plot_results():
    pass

if __name__ == "__main__":
    debug_mode = "--debug" in sys.argv
    run_simulation(debug_mode=debug_mode)
