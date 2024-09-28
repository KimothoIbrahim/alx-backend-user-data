#!/usr/bin/env python3

from requests import request


base_url = "http://localhost:5000/"


def register_user(email: str, password: str) -> None:
    response = request('POST', f'{base_url}users',
                       data={'email': email, 'password': password})
    assert response.status_code == 200
    assert response.json() == {"email": f"{email}",
                               "message": "user created"}

    response = request('POST', f'{base_url}users',
                       data={'email': email, 'password': password})
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    response = request('POST', f'{base_url}sessions',
                       data={'email': email, 'password': password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    response = request('POST', f'{base_url}sessions',
                       data={'email': email, 'password': password})
    assert response.status_code == 200
    assert response.json() == {"email": email,
                               "message": "logged in"}
    print(response.cookies['session_id'])
    return response.cookies['session_id']


def profile_logged(session_id: str) -> None:
    cookie = {'session_id': session_id}
    response = request('GET', f'{base_url}profile', cookies=cookie)
    assert response.status_code == 200
    assert response.json()


def profile_unlogged() -> None:
    response = request('GET', f'{base_url}profile')
    assert response.status_code == 403


def log_out(session_id: str) -> None:
    response = request('DELETE', f'{base_url}sessions',
                       cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    response = request('POST', f'{base_url}reset_password',
                       data={'email': email})
    assert response.status_code == 200
    assert response.json()
    return response.json()['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    response = request('PUT', f'{base_url}reset_password',
                       data={'email': email, 'reset_token': reset_token,
                             'new_password': new_password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

print("Completed")
