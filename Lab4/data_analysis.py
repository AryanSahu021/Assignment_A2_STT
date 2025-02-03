import pandas as pd
import matplotlib.pyplot as plt
import os
from py2cfg import CFGBuilder
from PIL import Image
import sys
from pydriller import Repository
import shutil

# Load the CSV file
csv_file = sys.argv[1] + '_results/commits_info.csv'
df = pd.read_csv(csv_file)

# Task 1: Identify and report the top 3 frequently changed source code files
file_change_counts = df['new_file path'].value_counts().head(3)
print("Top 3 frequently changed source code files:")
print(file_change_counts)

# Task 2: For the most frequently changed Python file, show how its CFG changes
most_frequent_py_file = file_change_counts.index[0]  # Get the most frequently changed file
if most_frequent_py_file.endswith('.py'):
    print(f"\nMost frequently changed Python file: {most_frequent_py_file}")
    
    # Filter commits for the most frequently changed Python file
    file_commits = df[df['new_file path'] == most_frequent_py_file]
    
    # Generate CFG for each commit
    cfg_images = []
    for index, row in file_commits.iterrows():
        commit_hash = row['commit SHA']
        
        # Use PyDriller to checkout the commit
        repo_path = sys.argv[1]
        temp_repo_path = f"{repo_path}_temp_{commit_hash}"
        if os.path.exists(temp_repo_path):
            shutil.rmtree(temp_repo_path)
        
        # Clone the repository (if not already cloned)
        # Checkout the specific commit
        repo = Repository(repo_path, single=commit_hash)
        for commit in repo.traverse_commits():
            # Copy the repository to a temporary directory
            shutil.copytree(repo_path, temp_repo_path, dirs_exist_ok=True)
            break
        
        # Locate the file in the temporary repository
        file_path = os.path.join(temp_repo_path, most_frequent_py_file)
        
        if os.path.exists(file_path):
            # Generate CFG using py2cfg
            cfg_builder = CFGBuilder()
            cfg = cfg_builder.build_from_file(most_frequent_py_file, file_path)
            
            # Save the CFG as an image
            cfg_image_path = f"cfg_{commit_hash}.png"
            cfg.build_visual(cfg_image_path, format='png', show=False)
            cfg_images.append(cfg_image_path)
        else:
            print(f"File {most_frequent_py_file} not found in commit {commit_hash}")
        
        # Clean up the temporary repository
        shutil.rmtree(temp_repo_path)
    
    # Combine all CFG images into one page (scaled down)
    
# Task 3: Plot the changes of cyclomatic complexity values along the timeline
# Use the row index as a proxy for the commit sequence
df['commit_sequence'] = df.index

plt.figure(figsize=(10, 6))
for file in file_change_counts.index:
    file_data = df[df['new_file path'] == file]
    plt.plot(file_data['commit_sequence'], file_data['new_mcc'], label=file)

plt.xlabel('Commit Sequence')
plt.ylabel('Cyclomatic Complexity')
plt.title('Cyclomatic Complexity Changes Over Commit Sequence')
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig('cyclomatic_complexity_trend.png', dpi=300)
print("Cyclomatic complexity trend plot saved to cyclomatic_complexity_trend.png")

