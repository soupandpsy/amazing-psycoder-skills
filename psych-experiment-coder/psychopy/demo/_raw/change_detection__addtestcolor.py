# Source: change_detection (demos/change_detection)
# Project URL: https://gitlab.pavlovia.org/demos/change_detection
# Original file: code/addtestcolor.py
import pandas as pd
import numpy as np
import random

# Example named colors
named_colors = [
    "red", "blue", "green", "yellow", "orange",
    "purple", "cyan", "magenta", "pink", "brown"
]

# Load your spreadsheet (replace 'your_spreadsheet.xlsx' with your actual file)
df = pd.read_csv('localisation_trials.csv')

# Create new test color columns and a changed color index column
for i in range(1, 7):  # For color1 to color6
    test_col_name = f'testcolor{i}'
    df[test_col_name] = df[f'color{i}']  # Start with the same color

# Add a column to track the changed color index
df['changed_color_index'] = np.nan  # Initialize with NaN

# Iterate through each row
for index, row in df.iterrows():
    # Select a random column to replace (color1 to color6)
    color_col_index = random.randint(1, 6)
    selected_color_col = f'color{color_col_index}'
    
    # Get the current colors in the row
    current_colors = set(row[f'color{j}'] for j in range(1, 7))
    
    # Find a color not already in the current row
    available_colors = list(set(named_colors) - current_colors)
    
    if available_colors:  # Check if there are available colors
        new_color = random.choice(available_colors)
        # Replace the selected color with the new color in the test column
        df.at[index, f'testcolor{color_col_index}'] = new_color
        
        # Record which color index was changed
        df.at[index, 'changed_color_index'] = color_col_index

# Save the modified DataFrame back to a new spreadsheet
df.to_excel('localisation_trials_with_test_columns.xlsx', index=False)

