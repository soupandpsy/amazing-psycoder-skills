# Source: change_detection (demos/change_detection)
# Project URL: https://gitlab.pavlovia.org/demos/change_detection
# Original file: code/generate_locations.py
import math
import csv
import random

def calculate_circle_points(radius, num_points):
    points = []
    angle_increment = 2 * math.pi / num_points  # Divide the circle into equal parts
    for i in range(num_points):
        angle = i * angle_increment
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append((x, y))
    return points

# Function to sample 6 points from the 8 generated points, 10 times
def sample_points(points, num_samples, num_iterations):
    all_samples = []
    for _ in range(num_iterations):
        # Randomly sample 6 points without replacement
        sampled_points = random.sample(points, num_samples)
        # Flatten the sampled points to create a single row with 12 columns (x1, y1, x2, y2, ..., x6, y6)
        flattened = [coord for point in sampled_points for coord in point]
        all_samples.append(flattened)
    return all_samples

# Function to sample 6 colors from a list of colors, 10 times
def sample_colors(color_list, num_samples, num_iterations):
    all_color_samples = []
    for _ in range(num_iterations):
        # Randomly sample 6 colors without replacement
        sampled_colors = random.sample(color_list, num_samples)
        all_color_samples.append(sampled_colors)
    return all_color_samples

# List of named colors (10 examples)
named_colors = [
    "red", "blue", "green", "yellow", "orange",
    "purple", "cyan", "magenta", "pink", "brown"
]

# Radius of the circle
radius = 0.3
# Number of points to calculate (8 in this case)
num_points = 8
# Number of points to sample (6 each time)
num_samples = 6
# Number of iterations (10 in this case)
num_iterations = 10

# Get the coordinates of the 8 points on the circle
circle_points = calculate_circle_points(radius, num_points)

# Sample points 10 times
sampled_data = sample_points(circle_points, num_samples, num_iterations)
# Sample colors 10 times
sampled_colors = sample_colors(named_colors, num_samples, num_iterations)

# Define the output file name
output_file = "sampled_circle_points_with_colors.csv"

# Save the sampled coordinates and colors to a CSV file
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    header = []
    for i in range(num_samples):
        header.append(f"x{i + 1}")
        header.append(f"y{i + 1}")
    header += [f"color{i + 1}" for i in range(num_samples)]  # Add color headers
    writer.writerow(header)
    
    # Write each row of sampled coordinates and colors
    for i in range(num_iterations):
        writer.writerow(sampled_data[i] + sampled_colors[i])  # Combine points and colors

print(f"Sampled coordinates and colors have been saved to {output_file}")

