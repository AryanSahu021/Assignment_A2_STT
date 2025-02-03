import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('line_profiler_results/commits_info.csv')

# Define a function to check if a file is a code artifact
def is_code_artifact(file_path):
    code_extensions = ['.py', '.java', '.cpp', '.c', '.js', '.html', '.css']  # Add more extensions if needed
    return any(file_path.endswith(ext) for ext in code_extensions) if pd.notna(file_path) else False

# Classify rows into code and non-code artifacts
df['is_code'] = df['new_file path'].apply(is_code_artifact)

# Calculate the number of matches and no matches for code and non-code artifacts
matches_code = df[(df['is_code'] == True) & (df['matches'] == 'YES')].shape[0]
no_matches_code = df[(df['is_code'] == True) & (df['matches'] == 'NO')].shape[0]
matches_non_code = df[(df['is_code'] == False) & (df['matches'] == 'YES')].shape[0]
no_matches_non_code = df[(df['is_code'] == False) & (df['matches'] == 'NO')].shape[0]

# Data for plotting
categories = ['Matches (Code)', 'No Matches (Code)', 'Matches (Non-Code)', 'No Matches (Non-Code)']
values = [matches_code, no_matches_code, matches_non_code, no_matches_non_code]

# Plotting
plt.figure(figsize=(10, 6))
bars = plt.bar(categories, values, color=['blue', 'orange', 'green', 'red'])

# Adding the value labels on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2., height, f'{int(height)}', ha='center', va='bottom')

plt.xlabel('Categories')
plt.ylabel('Count')
plt.title('Comparison of Matches and No Matches for Code and Non-Code Artifacts')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot
plt.savefig('matches_comparison.png')

# Show the plot
plt.show()