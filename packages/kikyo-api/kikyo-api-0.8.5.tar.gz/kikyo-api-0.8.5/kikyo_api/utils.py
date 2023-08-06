from requests import Response

from kikyo_api.errors import KikyoClientError


def read_json_data(resp: Response) -> dict:
    raise_client_error(resp)
    return resp.json()['data']


def raise_client_error(resp: Response):
    try:
        resp.raise_for_status()
    except Exception:
        try:
            data = resp.json()
        except Exception:
            pass
        else:
            if 'msg' in data:
                raise KikyoClientError(resp.status_code, data['msg'])
        raise
