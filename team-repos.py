#!/usr/bin/env python3
from github import Github
import sys
# First create a Github instance:
# using an access token
g = Github("token")
organization = g.get_organization('GH_org')

team_search = input("What team do you want to see teams/repos for? ")
sub_orgs = organization.get_teams()
for sub_org in sub_orgs:
	if sub_org.name == team_search:
		team = organization.get_team(sub_org.id)
# print primary team name, format uses a variable wherever you would have {}
print("Primary team is: {}".format(team.name))
#
for sub_team in team.get_teams():
	print('-----------------')
	print("    Sub team is: {}".format(sub_team.name))
	sub_team_repos = sub_team.get_repos()
	print("        Repos under this team below: \n")
	for repo in sub_team_repos:
		print("            Repo name is {}".format(repo.name))

