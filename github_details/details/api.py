import asyncio
import os
import aiohttp
import logging
import itertools
from flask_restplus import Namespace, Resource, reqparse

logger = logging.getLogger(__name__)

api = Namespace('', description='User & repo details API')

request_url = 'https://api.github.com'
token = os.environ.get('GITHUB_TOKEN')
headers = {'Accept': 'application/vnd.github.v3+json',
           'Authorization': f'token {token}'}


async def call(session, url):
    if not url:
        return
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            logger.info(f'Successfully got {url}')
            return await response.json()
    except Exception as e:
        logger.error(f'Unable to get {url} due to {e.__class__}.')


async def make_requests(user_urls, event_urls):
    async with aiohttp.ClientSession(headers=headers) as session:
        first = asyncio.gather(*(call(session, url) for url in user_urls))
        second = asyncio.gather(*(call(session, url) for url in event_urls))
        return await first, await second


@api.route('')
class GitHubDetails(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('usernames', action='split', location='args')
    parser.add_argument('include', required=False, action='append')

    @staticmethod
    def extract_repo(repo):
        return {'repo_name': repo['full_name'],
                'id': repo['id'],
                'created_at': repo['created_at'],
                'updated_at': repo['updated_at'],
                'resource_uri': repo['html_url']}

    def build_repo(self, username, user_run, events_run):
        repo_dict = {}

        if user_run:
            repo_list = sorted(map(self.extract_repo, user_run), key=lambda i: i['updated_at'], reverse=True)
            owner = user_run[0]['owner']
            repo_dict = {'login_name': owner['login'],
                         'user_id': owner['id'],
                         'resource_uri': owner['html_url'],
                         'public_repos': repo_list}

        logger.info(f'Fetched repo info for username {username}')

        if events_run:
            event = next((event for event in events_run if event['type'] == 'PushEvent'), None)
            if event:
                commit = event['payload']['commits'][0]
                event = {'commit_hash': commit['sha'],
                         'author': commit['author']['name'],
                         'committer-email': commit['author']['email'],
                         'commit-date': event['created_at'],
                         'resource-uri': commit['url']}
                repo_dict.update({'latest_commit': event})

            logger.info(f'Fetched events for username {username}')

        return repo_dict

    def get(self):
        params = self.parser.parse_args()
        include, usernames = params['include'], list(filter(None, params['usernames']))

        user_urls = [request_url + f'/users/{username}/repos?per_page=50' for username in usernames]
        events_urls = [request_url + f'/users/{username}/received_events' if include else None
                       for username in usernames]

        user_runs, events_runs = asyncio.run(make_requests(user_urls, events_urls))

        return list(itertools.starmap(self.build_repo, zip(usernames, user_runs, events_runs)))
