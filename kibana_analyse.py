import json
import re
import time
from collections import Counter

import requests


def search(request: str, session_):
    cont_ = session_.post(
        'https://monitor-otr.mercedes-benz.com.cn/internal/bsearch',
        data=request,
        headers={'kbn-version': '7.16.2'}
    )
    new_request = json.loads(request)
    if 'id' in cont_.json()['result']:
        time.sleep(5)
        new_request['batch'][0]['request']['id'] = cont_.json()['result']['id']
        return session_.post(
            'https://monitor-otr.mercedes-benz.com.cn/internal/bsearch',
            data=json.dumps(new_request),
            headers={'kbn-version': '7.16.2'}
        )
    else:
        return cont_


def get_failed_requests(request, size):
    session = requests.session()

    # login, init cookie
    data = {"providerType": "basic", "providerName": "basic",
            "currentURL": "https://monitor-otr.mercedes-benz.com.cn/login?next=%2F",
            "params": {"username": "xxx", "password": "xxx"}}
    headers = {'kbn-version': '7.16.2'}
    session.post(
        url='https://monitor-otr.mercedes-benz.com.cn/internal/security/login',
        headers=headers,
        data=json.dumps(data)
    )

    # failed request
    failed_request_request = json.loads(request)
    failed_request_request['batch'] = [item for item in failed_request_request['batch'] if item['options']['executionContext']['description'] == 'fetch documents']
    failed_request_request['batch'][0]['request']['params']['body']['size'] = size
    cont = search(json.dumps(failed_request_request), session)
    hits_ = cont.json()['result']['rawResponse']['hits']['hits']
    print(len(hits_))
    hits_ = [item['fields']['request'][0] for item in hits_]
    hits_ = [re.sub(r'/\w*?\d+\w*?$', '/xxx', item) for item in hits_]
    hits_ = [re.sub(r'/\w*?\d+\w*?\?', '/xxx?', item) for item in hits_]
    hits_ = [re.sub(r'/\w*?\d+\w*?/', '/xxx/', item) for item in hits_]
    hits_ = [re.sub(r'=\w*?\d+\w*?$', '=xxx', item) for item in hits_]
    hits_ = [re.sub(r'=\w*?\d+\w*?&', '=xxx&', item) for item in hits_]
    hits_counter = Counter(hits_)
    hits_counter = hits_counter.most_common()
    return len(hits_), hits_counter
