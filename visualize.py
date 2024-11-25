import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

plt.rcParams['figure.figsize'] = (12.0, 9.0)

# Preprocessing Input data
data = pd.read_csv('out.csv')

# Extract followers and like count columns
followers = data['followers']
like_count = data['Like Count']

# Calculate the IQR for followers and like count
Q1_followers = followers.quantile(0.25)
Q3_followers = followers.quantile(0.75)
IQR_followers = Q3_followers - Q1_followers

Q1_like_count = like_count.quantile(0.25)
Q3_like_count = like_count.quantile(0.75)
IQR_like_count = Q3_like_count - Q1_like_count

# Define outlier thresholds for followers and like count
lower_limit_followers = Q1_followers - 1.5 * IQR_followers
upper_limit_followers = Q3_followers + 1.5 * IQR_followers

lower_limit_like_count = Q1_like_count - 1.5 * IQR_like_count
upper_limit_like_count = Q3_like_count + 1.5 * IQR_like_count

# Filter out outliers and apply additional constraints (followers < 200000, Like Count < 50000)
filtered_data = data[
    (followers >= lower_limit_followers) & (followers <= upper_limit_followers) &
    (like_count >= lower_limit_like_count) & (like_count <= upper_limit_like_count) &
    (followers < 100000) & (like_count < 10000)
]

# Extract the filtered followers and like count columns
filtered_followers = filtered_data['followers'].values.reshape(-1, 1)  # Reshaped for regression
filtered_like_count = filtered_data['Like Count'].values

# Perform Linear Regression
model = LinearRegression()
model.fit(filtered_followers, filtered_like_count)

# Get the slope (m) and intercept (b) of the best fit line
slope = model.coef_[0]
intercept = model.intercept_

# Predict the like count values using the best fit line
predicted_like_count = model.predict(filtered_followers)

# Create a scatter plot with the filtered data
plt.scatter(filtered_followers, filtered_like_count, color='blue', alpha=0.7)

# Plot the best fit line
plt.plot(filtered_followers, predicted_like_count, color='red', linewidth=2, label=f'Best Fit Line (y = {slope:.2f}x + {intercept:.2f})')

# Title and labels
plt.title('Followers vs Like Count (Outliers Removed, Followers < 200000, Like Count < 50000)')
plt.xlabel('Followers')
plt.ylabel('Like Count')
plt.grid(True)
plt.legend()

# Show the plot
plt.show()
