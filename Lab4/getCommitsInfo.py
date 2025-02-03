import sys
import csv
from pydriller import Repository
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.commits_count import CommitsCount
from pydriller.metrics.process.hunks_count import HunksCount

columns = ["old_file path", "new_file path", "commit SHA", "parent commit SHA", "commit message", "diff", "old_mcc", "new_mcc"]

rows = []
count = 0
last_n = 500

commits = []
for x in Repository(sys.argv[1], only_no_merge=True, order='reverse').traverse_commits():
    if x.in_main_branch:
        count += 1
        commits.append(x)
        if count == last_n:
            break

in_order = []
for value in range(len(commits)):
    in_order.append(commits.pop())

commits = in_order
i = -1
for commit in commits:
    i += 1
    print('[{}/{}] Mining commit {}.{}'.format(i + 1, len(commits), sys.argv[1], commit.hash))
    
    for m in commit.modified_files:
        # Get the complexity after the commit
        new_mcc = m.complexity if m.complexity else 0
        
        # Get the complexity before the commit by looking at the parent commit
        old_mcc = 0
        if commit.parents:
            parent_commit_hash = commit.parents[0]
            parent_commit = Repository(sys.argv[1], single=parent_commit_hash).traverse_commits().__next__()
            for parent_file in parent_commit.modified_files:
                if parent_file.new_path == m.new_path or parent_file.old_path == m.old_path:
                    old_mcc = parent_file.complexity if parent_file.complexity else 0
                    break
        
        if len(commit.parents) > 0:
            parent = commit.parents[0]
        else:
            parent = None
        
        rows.append([str(m.old_path), str(m.new_path), str(commit.hash), str(parent), str(commit.msg), str(m.diff), old_mcc, new_mcc])

with open(sys.argv[1] + '_results/commits_info.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(columns)
    writer.writerows(rows)