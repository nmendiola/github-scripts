#!/usr/bin/env python3
from github import Github
import pandas as pd
import argparse
import pprint
import requests
from tqdm import tqdm

# First create a Github instance:
# using an accessteam = []

pp = pprint.PrettyPrinter(indent=4)
parser = argparse.ArgumentParser(description='I DO STUFF')
parser.add_argument('-t', '--token', help='Token we are using to authenticate', required=True)
parser.add_argument('-o', '--organization', help='Organization we are searching', required=True)
args = parser.parse_args()
g = Github(args.token)
organization = g.get_organization(args.organization)
auth_headers = {'Accept': 'application/vnd.github.nebula-preview+json', 'Authorization': 'token ' + args.token}
team_df = pd.DataFrame(columns=['Group Visible Name', 'Path', 'Group Visibility'])
repo_df = pd.DataFrame(columns=['Source url', 'Target group path', 'Project Visible Name', 'Project path', 'Project Visibility'])

team_search = input("What team do you want get info on? ")
sub_orgs = organization.get_teams()
for sub_org in sub_orgs:
	if sub_org.name == team_search:
		root_team = organization.get_team(sub_org.id)
# print primary team name, format uses a variable wherever you would have {}
# print("Primary team is: {}".format(root_team.name))
team_df = team_df.append({'Group Visible Name': root_team.name, 'Path': root_team.slug, 'Group Privacy': root_team.privacy}, ignore_index=True)

#
for sub_team in root_team.get_teams():
	# print('-----------------')
	# print("    Sub team is: {}".format(sub_team.name))
	team_df = team_df.append({'Group Visible Name': root_team.name, 'Path': '{}/{}'.format(root_team.slug, sub_team.slug), 'Group Privacy': sub_team.privacy}, ignore_index=True)
	sub_team_repos = sub_team.get_repos()
	print('Scanning repos for {}'.format(sub_team.name))
	repo_count = sub_team.repos_count
	for repo in tqdm(sub_team_repos, total=repo_count):
		repo_url = repo.url
		r = requests.get(repo_url, headers=auth_headers)
		sub_team_visibility = r.json()['visibility']
		repo_df = repo_df.append({'Source url': repo.ssh_url, 'Target group path': '{}/{}'.format(root_team.slug, sub_team.slug), 'Project Visible Name': repo.name, 'Project path': repo.full_name, 'Project Visibility': sub_team_visibility}, ignore_index=True)
		# print("            Repo name is {}".format(repo.name))


team_df.to_csv('team_list.csv', index=False)
repo_df.to_csv('repo_list.csv', index=False)

