"""
Interacting with WolframAlpha

The API documentation is in PDF format here -> https://products.wolframalpha.com/docs/WolframAlpha-API-Reference.pdf
"""

from __future__ import annotations

import requests


class WolframAlphaServices:
    """
    A class wrapping WolframAlpha's API.
    """

    def __init__(
        self,
        base_url: str,
        app_id: str,
    ):
        self.base_url: str = base_url
        self.__app_id: str = app_id

    def _make_request(
        self,
        method: str,
        action: str,
        params: list[tuple[str, str]] = None,
        timeout: int = 500,
    ) -> dict:
        """Make a request to WolframAlpha's API"""
        if params is None:
            params = []
        params.append(("appid", self.__app_id))

        args = {
            "method": method,
            "url": self.base_url + action,
            "params": params,
            "timeout": timeout,
        }

        response = requests.request(**args)
        return response.json()

    def query(
        self,
        query: str,
    ) -> dict:
        """query endpoint"""
        params = [
            ("input", query),
            ("format", "image,plaintext"),
            ("output", "JSON"),
        ]
        return self._make_request(method="GET", action="query", params=params)
