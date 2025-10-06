from httpx import Request, RequestNotRead


def make_curl_from_request(request: Request) -> str:
    """
    Generates the cURL command from an httpx HTTP request.

    :param request: An HTTP request from which the cURL command will be generated.
    :return: A string with the cURL command containing the request method, URL, headers, and body (if any).
    """
    result: list[str] = [f"curl -X '{request.method}'", f"'{request.url}'"]

    for header, value in request.headers.items():
        result.append(f"-H '{header}: {value}'")

    try:
        if body := request.content:
            result.append(f"-d '{body.decode('utf-8')}'")
    except RequestNotRead:
        pass

    return " \\\n  ".join(result)
