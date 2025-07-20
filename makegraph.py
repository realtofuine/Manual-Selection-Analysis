import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D


# === STEP 1: Load the CSV file ===
def plot(option):
    csv_file = '/Users/rishi/Downloads/28.csv'  # Replace with your actual filename
    df = pd.read_csv(csv_file)

    # === STEP 3: (Optional) Filter for confident detections ===

    # Only include rows where yolk was confidently detected (likelihood > 0.5)
    df = df[(df['prob_Y'] > 0.5)]

    if option == 'all':
        wells = sorted(df['Well'].unique())
        num_wells = len(wells)

        cols = 3  # number of columns of plots (you can change this)
        rows = math.ceil(num_wells / cols)
        fig = plt.figure(figsize=(5 * cols, 5 * rows))

        for i, well in enumerate(wells, start=1):
            ax = fig.add_subplot(rows, cols, i, projection='3d')
            subset = df[df['Well'] == well]

            x = subset['X']
            y = subset['Y']
            z = subset['Image']

            ax.plot(x, y, z, label=f'Well {well}')
            ax.set_title(f'Well {well}')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Time')
            ax.legend()
    else:
        well = int(option)
        subset = df[df['Well'] == well]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        x = subset['X']
        y = subset['Y']
        z = subset['Image']

        ax.plot(x, y, z, label=f'Well {well}')
        ax.set_title(f'Well {well}')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Image')
        ax.legend()

    ax.set_box_aspect([1, 1, 2])  # Make Z axis taller visually
    plt.subplots_adjust(top=0.95, bottom=0.1, left=0.05, right=0.95)
    plt.show()


plot('4')