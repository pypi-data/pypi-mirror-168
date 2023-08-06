from datetime import date

import requests

from .util import sep


class Login:
    def __init__(self, name, token, gist_id, filename='gistats.ini'):
        self.token = token
        self.gist_id = gist_id
        self.filename = filename
        self.name = name

    def update(self, statistics, separator='.', until=15):
        content = sep(statistics, separator, until)
        response = requests.patch(
            url='https://api.github.com/gists/' + self.gist_id,
            json={
                'description': 'Updated on ' + str(date.today()),
                'files': {
                    self.filename: {'content': content}
                }
            },
            auth=(self.name, self.token)
        )

        return response.status_code
