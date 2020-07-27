This is a Python application developed with Flask and Python 3.7.2. It calls the `GitHub API` using Personal access token based
authentication. 

The application calls the GitHub API v3 and fetches user-related data in asynchronous way, using `asyncio` and `aiohttp`
libraries. It does not cache and does not store data, so no need to setup a database. 

To run the app: 
- create the virtual environment:
`virtualenv --no-site-packages -p python3.67.2 env`

- activate the virtual env: 
`. env/bin/activate`

- export Flask app:
`export FLASK_APP=github_details.web.wsgi`

- install dependencies: 
`pip install -e .`

- run it:
`python -m flask run`

The GET endpoint `/users` is setup as a Flask Restplus namespace resource and accepts a list of `usernames` 
comma-separated params and optional param `include`. 

A call to `/users?usernames=alhewpl,guneriu&include=latest_commit` will result in:
-  [
    {
-       "login_name": "alhewpl",
        "user_id": 7412572,
        "resource_uri": "https://github.com/alhewpl",
        "public_repos": [
            {
                "repo_name": "alhewpl/Movie-recommendation-system-with-Python",
                "id": 106670946,
                "created_at": "2017-10-12T09:14:54Z",
                "updated_at": "2020-06-01T14:49:13Z",
                "resource_uri": "https://github.com/alhewpl/Movie-recommendation-system-with-Python"
            },
            {
                "repo_name": "alhewpl/Python-Data-Structures-Algorithms",
                "id": 152073066,
                "created_at": "2018-10-08T12:05:30Z",
                "updated_at": "2020-05-13T04:38:37Z",
                "resource_uri": "https://github.com/alhewpl/Python-Data-Structures-Algorithms"
            }
        ],
        "latest_commit": {
            "commit_hash": "544f334dc369de6718658c018e2e430b6600dfd9",
            "author": "Astrid Varga",
            "committer-email": "axxx.vxxa@gmx.de",
            "commit-date": "2020-07-03T20:09:22Z",
            "resource-uri": "https://api.github.com/repos/rubymonsters/rgbapp/commits/544f334dc369de6718658c018e2e430b6600dfd9"
        },
       {
        "login_name": "guneriu",
        "user_id": 1208079,
        "resource_uri": "https://github.com/guneriu",
        "public_repos": [
            {
                "repo_name": "guneriu/customization-engine",
                "id": 215763661,
                "created_at": "2019-10-17T10:16:35Z",
                "updated_at": "2019-10-17T10:16:35Z",
                "resource_uri": "https://github.com/guneriu/customization-engine"
            },
            {
                "repo_name": "guneriu/terraform-aws-vpc",
                "id": 168995279,
                "created_at": "2019-02-03T21:25:34Z",
                "updated_at": "2019-02-03T21:25:36Z",
                "resource_uri": "https://github.com/guneriu/terraform-aws-vpc"
            },
        ],
        "latest_commit": null    

 
Assumptions I've made: 
-  To fetch the latest commit, instead of going through the repo list per each user, I'm calling the 
` https://api.github.com/users/{username}/received_events` api and filtering by `PushEvent` type. This will get me the 
most recent commit done on any branch, any repo the user is subscribed to. These are ordered by creation time, from 
latest to oldest. 

- I've used the info level logging to exemplify the async call times

- I've chosen not to setup a database as the information is publicly available and with authentication can be called up 
to 5000 times, but it also contains sensitive data like email that needs to be encoded. 
