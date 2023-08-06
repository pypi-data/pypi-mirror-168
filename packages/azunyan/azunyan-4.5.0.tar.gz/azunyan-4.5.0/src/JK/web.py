import requests


session = requests.Session()


def get(url, params={}, headers={}, cookies={}, timeout=15, retry=3) -> requests.Response:
    for c in range(retry):
        r = session.get(url, params=params, headers=headers, cookies=cookies, timeout=timeout)
        if 200 <= r.status_code <= 299:
            return r
    return r


def post(url, params={}, data='', headers={}, cookies={}, timeout=15, retry=3):
    for c in range(retry):
        r = session.post(url, params=params, data=data, headers=headers, cookies=cookies, timeout=timeout)
        if 200 <= r.status_code <= 299:
            return r
    return r


# def get(url, params={}, headers={}, cookies={}, timeout=15, retry=3, debug=False) -> requests.Response:
#     for c in range(retry):
#         try:
#             r = session.get(url, params=params, headers=headers, cookies=cookies, timeout=timeout)
#             r.raise_for_status()
#             return r
#         except requests.exceptions.HTTPError as err:
#             if not debug:
#                 print(F'({c+1}/{retry}) Http Error: {r.status_code}')
#             else:
#                 print(F'({c+1}/{retry}) Http Error:\n==========\n{err}\n{err.response.text}\n==========')
#         except requests.exceptions.ConnectionError as err:
#             if not debug:
#                 print(F'({c+1}/{retry}) Connection Error: {r.status_code}')
#             else:
#                 print(F'({c+1}/{retry}) Connection Error:\n==========\n{err}\n==========')
#         except requests.exceptions.Timeout as err:
#             if not debug:
#                 print(F'({c+1}/{retry}) Timeout Error: {r.status_code}')
#             else:
#                 print(F'({c+1}/{retry}) Timeout Error:\n==========\n{err}\n==========')
#         except requests.exceptions.TooManyRedirects as err:
#             if not debug:
#                 print(F'({c+1}/{retry}) Too Many Redirects Error: {r.status_code}')
#             else:
#                 print(F'({c+1}/{retry}) Too Many Redirects Error:\n==========\n{err}\n==========')
#         except requests.exceptions.RequestException as err:
#             if not debug:
#                 print(F'({c+1}/{retry}) Request Exception Error: {r.status_code}')
#             else:
#                 print(F'({c+1}/{retry}) Request Exception Error:\n==========\n{err}\n==========')
#     print('rGET failed')
