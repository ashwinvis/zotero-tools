# coding: utf-8
import random
import time
from pygithub import Github

# Ref:
# https://pygithub.readthedocs.io/en/latest/introduction.html#very-short-tutorial
# If you are using an access token to circumvent 2FA, make sure you have
# enabled "repo" scope
g = Github("username", "password")

me = g.get_user()
starred = me.get_starred()
for repo in starred:
    print("Unstarring", repo)
    me.remove_from_starred(repo)
    time.sleep(1 + random.random())  # try to avoid rate-limit

# Troubleshooting
# https://developer.github.com/v3/activity/starring/#unstar-a-repository
# Debug using curl:
# $ curl -H "Authorization: token $INSERT_ACCESS_TOKEN" \
#    "https://api.github.com/user/starred/<owner>/<repo>" -i -s -X DELETE
