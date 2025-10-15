import base64

UTF8 = "utf-8"


def generate_basic_auth_header(username: str, password: str) -> str:
    """
    Create a Basic Auth header for HTTP requests.
    :param username: The username for Basic Auth.
    :param password: The password for Basic Auth.
    :return: The Basic Auth header string.
    """
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode(UTF8)).decode(UTF8)
    return f"Basic {encoded_credentials}"
