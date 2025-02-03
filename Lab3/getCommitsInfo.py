import sys
import csv
from pydriller import Repository
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.commits_count import CommitsCount
from pydriller.metrics.process.hunks_count import HunksCount
columns = ["old_file path" ,"new_file path" ,"commit SHA" ,"parent commit SHA","commit message","diff_myers1", "diff_hist2", "matches"]

rows = []
count=0
last_n=500

commits = []
for x,y in zip(Repository(sys.argv[1],only_no_merge=True,order='reverse').traverse_commits(), Repository(sys.argv[1], only_no_merge=True, histogram_diff = True, order='reverse').traverse_commits()):
  if (x.in_main_branch==True and y.in_main_branch):
    count=count+1
    commits.append([x, y])
    if count == last_n:
      break

in_order = []
for value in range(len(commits)):
  in_order.append(commits.pop())

commits=in_order
i=-1
for commit in commits:
  i+=1
  print('[{}/{}] Mining commit {}.{}'.format(i+1,len(commits),sys.argv[1],commit[0].hash))
  for m1, m2 in zip(commit[0].modified_files, commit[1].modified_files):
    if m1.diff_parsed == m2.diff_parsed: 
      matches = "YES"
    else:
      matches = "NO"
    if len(commit[0].parents) > 0:
      parent = commit[0].parents[0]
    else:
      parent = None
    rows.append([str(m1.old_path), str(m1.new_path), str(commit[0].hash), str(parent), str(commit[0].msg), str(m1.diff_parsed), str(m2.diff_parsed), matches])
    # diff.append(m.diff_parsed)
      
  # if (i>=1):   
  #   rows.append([commit.hash,commit.msg,diff])
  # elif (i==0):
  #   rows.append([commit.hash,commit.msg,''])
       
with open(sys.argv[1]+'_results/commits_info.csv', 'a') as csvFile:
  writer = csv.writer(csvFile)
  writer.writerow(columns)
  writer.writerows(rows)
