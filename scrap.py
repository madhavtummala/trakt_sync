import os
import time
from datetime import datetime
from prettytable import PrettyTable

# Movies 
movies = PrettyTable(['Title', 'Year', 'Watched at'])
shows = PrettyTable(['Title', 'Watched at'])

path = os.walk("/Volumes/Backup Plus/Movies")

count = 0
for root, directories, files in path:
	if "(" in root and ")" in root.split("/")[-1]:
		try:
			count += 1
			name = root.split("/")[-1]
			title, year = name.split("(")
			year = year.split(")")[0]
			timetup = time.gmtime(os.stat(root).st_birthtime)
			watched_at = datetime(*timetup[:6]).isoformat(timespec='milliseconds') + 'Z'
		except:
			print(root)
			print(name)
			timetup = time.gmtime(os.stat(root).st_birthtime)
			watched_at = datetime(*timetup[:6]).isoformat(timespec='milliseconds') + 'Z'
			print(watched_at)


		# print(title, year, watched_at)
		movies.add_row([title, year, watched_at])

print(movies)
print(count)

# Shows

count = 0
path = os.walk("/Volumes/Backup Plus/TV SERIES")

for root, directories, files in path:
	# print(root, len(root.split("/")))
	if len(root.split("/")) == 6:
		count += 1;
		title = root.split("/")[-1]
		if title =="krpkeb":
			continue
		timetup = time.gmtime(os.stat(root).st_birthtime)
		watched_at = datetime(*timetup[:6]).isoformat(timespec='milliseconds') + 'Z'
		# print(title, watched_at)
		shows.add_row([title, watched_at])

print(shows)
print(count)

