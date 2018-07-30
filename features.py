# Native imports
import argparse
import json
import os
from pathlib import Path
from subprocess import check_output
import sys
import webbrowser

# Installed imports
import requests
from dateutil.parser import parse

# Custom imports
from color import pRed, pGreen


# Load configuration
CONFIG = str(Path.home()) + "/.github-cli.json"
with open(CONFIG) as configFile:
    config = json.load(configFile)

BASE_API_URL = "https://api.github.com{}"
BASE_WEB_URL = "https://github.com{}"
AUTH = {
    "Authorization": "token " + config['token']
}

class GitHub(object):

    def __init__(self, desc):
        parser = argparse.ArgumentParser(
            description=desc)
        parser.add_argument('command')
        args = parser.parse_args(sys.argv[2:3])

        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        getattr(self, args.command)()

class Repository(GitHub):
    
    def __init__(self):
        super(Repository, self).__init__('Interact with your repositories')

    def open(self):
        parser = argparse.ArgumentParser(
            description='Open a repository on github webpage. Default: current')
        parser.add_argument("--name", help='Specify repository name')
        parser.add_argument("--owner", help='Specify repository owner')

        args = parser.parse_args(sys.argv[3:])

        owner = args.owner if args.owner else config["owner"]

        url = BASE_WEB_URL.format("/{}/".format(owner))

        if args.name:
            url += args.name
        else:
            cmdRepo = 'git config --get remote.origin.url'
            tmpName = check_output(cmdRepo, shell=True).decode('utf-8').strip()

            # Remove .git part
            url += str(tmpName.split("/")[-1][0:-4])

        webbrowser.open_new_tab(url)


class PullRequest(GitHub):

    def __init__(self):
        super(PullRequest, self).__init__('Interact with pull requests')

    def ls(self):
        parser = argparse.ArgumentParser(
            description='List pull requests from your repositories')
        parser.add_argument("--user", help='Filter results by user')

        args = parser.parse_args(sys.argv[3:])

        owner = config["owner"]
        pr_path = "/repos/" + owner + "/{}/pulls"
        reviews_path = pr_path + "/{}/reviews"

        for repository in config["repositories"]:
            pr_endpoint = BASE_API_URL.format(pr_path.format(repository))
            response = requests.get(pr_endpoint, headers=AUTH)

            pullRequests = response.json()

            if args.user:
                pullRequests = list(
                    filter(
                        lambda pr: pr["user"]["login"] == args.user,
                        pullRequests
                    )
                )

            pullRequests.sort(key=lambda x: x['updated_at'])

            if len(pullRequests):
                pRed("Pull requests para {}".format(repository))
                for pr in pullRequests:
                    r_endpoint = BASE_API_URL.format(
                                  reviews_path.format(repository, pr['number']))
                    reviews_reponse = requests.get(r_endpoint, headers=AUTH)
                    reviews = reviews_reponse.json()

                    if len(reviews):
                        review = reviews[-1]['state']
                    else:
                        review = "WAITING_REVIEW"

                    updated_at = parse(pr['updated_at'])
                    pGreen("\tCreator: ", end="")
                    print(pr['user']['login'])
                    pGreen("\tTitle: ", end="")
                    print(pr['title'])
                    pGreen("\tReview status: ", end="")
                    if review == "WAITING_REVIEW":
                        pRed(review)
                    else:
                        print(review)
                    pGreen("\tLast change: ", end="")
                    print('{} {}'.format(updated_at.date(), updated_at.time()))
                    pGreen("\tUrl: ", end="")
                    print(pr['html_url'], "\n")


FEATURES = {
    "pr": PullRequest,
    "repo": Repository
}
