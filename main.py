import requests
import json

import os
import time
from datetime import datetime

from secrets import my_client_id, access_token

def prepare_small_json(title, year, watched_at):
	my_movie = {}
	my_movie['watched_at'] = watched_at
	my_movie['title'] = title
	my_movie['year'] = int(year)

	my_json = {}
	my_json["movies"] = []
	my_json["movies"].append(my_movie)

	json_data = json.dumps(my_json)

	return json_data

def prepare_big_json(extra_local, media):
	my_json = {}
	my_json[media+"s"] = []
	for item in extra_local:
		my_obj = {}
		my_obj['watched_at'] = item[2]
		my_obj['title'] = item[0]
		if item[1] != None:
			my_obj['year'] = item[1]
		my_obj['ids'] = {}
		my_obj['ids']['trakt'] = item[3]
		my_json[media+"s"].append(my_obj)

	json_data = json.dumps(my_json)
	return json_data


def prepare_headers(access_token, my_client_id):
	headers = {}
	headers['Content-Type'] = 'application/json'
	headers['Authorization'] = access_token
	headers['trakt-api-version'] = '2'
	headers['trakt-api-key'] = my_client_id

	# headers_data = json.dumps(headers)
	return headers

def list_in_cloud(media):
	get_url = "https://api.trakt.tv/sync/history/{}/?limit=1000".format(media+"s")
	headers = prepare_headers(access_token, my_client_id)
	response = requests.get(get_url, headers=headers)
	items = response.json()
	return items

def list_in_local(media):
	if media == "movie":
		path = os.walk("/Volumes/Backup Plus/Movies")
		local_list = []
		for root, directories, files in path:
			if "(" in root and ")" in root.split("/")[-1]:
				try:
					name = root.split("/")[-1]
					title, year = name.split("(")
					year = year.split(")")[0]
					timetup = time.gmtime(os.stat(root).st_birthtime)
					watched_at = datetime(*timetup[:6]).isoformat(timespec='milliseconds') + 'Z'
					local_list.append([title.strip(), int(year.strip()), watched_at])
				except:
					continue

		return local_list
	else:
		path = os.walk("/Volumes/Backup Plus/TV SERIES")
		local_list = []
		for root, directories, files in path:
			if len(root.split("/")) == 6:
				title = root.split("/")[-1]
				if title =="krpkeb":
					continue
				timetup = time.gmtime(os.stat(root).st_birthtime)
				watched_at = datetime(*timetup[:6]).isoformat(timespec='milliseconds') + 'Z'
				# print(title, watched_at)
				local_list.append([title.strip(), None, watched_at])
		return local_list

def add_trakt_id_to_local_list(local_list, media):
	search_url = "https://api.trakt.tv/search/{}/".format(media)
	headers = prepare_headers(access_token, my_client_id)
	local_list_with_id = []
	for item in local_list:
		params = {'query' : item[0]}
		print("Searching {}({})".format(item[0], item[1]))
		response = requests.get(search_url, headers=headers, params = params)
		while response.status_code != 200:
			time.sleep(0.5)
			response = requests.get(search_url, headers=headers, params = params)
		found = False
		# print("Got {} results".format(len(response.json())))
		for i in response.json():
			if i[i['type']]['year'] == item[1]:
				item.append(i[i['type']]['ids']['trakt'])
				local_list_with_id.append(item)
				found = True
				break
		if not found and len(response.json()) > 0:
			i = response.json()[0]
			print("Couldn't find exact.. selecting {}({}) score:{}"
				.format(i[i['type']]['title'], i[i['type']]['year'], i['score']))
			item.append(i[i['type']]['ids']['trakt'])
			local_list_with_id.append(item)
	return local_list_with_id

def find_extra_in_local(original_cloud, original_local):
	cloud = [i[i['type']]['ids']['trakt'] for i in original_cloud]
	cloud_ids = list(set(cloud))
	extra_local = [i for i in original_local if i[3] not in cloud_ids]
	return extra_local

def add_to_cloud(extra_in_local, media):
	api_url = "https://api.trakt.tv/sync/history"
	for item in extra_in_local:
		headers = prepare_headers(access_token, my_client_id)
		json_data = prepare_small_json(extra_in_local, media)
		print("Uploading {} ({})".format(item[0],item[1]))
		response = requests.post(api_url, data=json_data, headers=headers)
		while(response.status_code != 201):
			time.sleep(0.5)
			response = requests.post(api_url, data=json_data, headers=headers)

def bulk_add_to_cloud(extra_in_local, media):
	api_url = "https://api.trakt.tv/sync/history"
	headers = prepare_headers(access_token, my_client_id)
	json_data = prepare_big_json(extra_in_local, media)
	print("Uploading Bulk {} items".format(len(extra_in_local)))
	response = requests.post(api_url, data=json_data, headers=headers)
	while(response.status_code != 201):
		time.sleep(0.5)
		response = requests.post(api_url, data=json_data, headers=headers)

media = "show"
local_list = list_in_local(media)
cloud_list = list_in_cloud(media)
local_list_with_id = add_trakt_id_to_local_list(local_list, media)
extra_local = find_extra_in_local(cloud_list, local_list_with_id)
bulk_add_to_cloud(extra_local, media)
























