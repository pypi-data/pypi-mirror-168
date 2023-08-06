import json
import requests


class ArvanClient:
    BASE_URL = "https://napi.arvancloud.com/ecc/v1/regions"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        try:
            _ = self.get_all_regions()
        except Exception as e:
            raise Exception("Invalid API key") from e

    def get_all_regions(self) -> list:
        return [x["code"] for x in self._send_request("GET", self.BASE_URL)["data"]]

    def get_servers_in_region(self, region: str) -> list:
        url = f"{self.BASE_URL}/{region}/servers"
        data = self._send_request("GET", url)["data"]
        return data

    def get_all_servers(self) -> list:
        regions = self.get_all_regions()
        servers = {}
        for region in regions:
            servers_in_region = self.get_servers_in_region(region)
            if servers_in_region:
                servers.update({region: servers_in_region})
        return servers

    def shutdown_server(self, region: str, server_id: str) -> None:
        url = f"{ArvanClient.BASE_URL}/{region}/servers/{server_id}/power-off"
        _ = self._send_request("POST", url)

    def turn_on_server(self, region: str, server_id: str) -> None:
        url = f"{ArvanClient.BASE_URL}/{region}/servers/{server_id}/power-on"
        _ = self._send_request("POST", url)

    def _all_servers_do(self, function: callable, onerror: callable = lambda r, s: None) -> None:
        servers = self.get_all_servers()
        for region, servers_in_region in servers.items():
            for server in servers_in_region:
                try:
                    function(region, server)
                except:
                    onerror(region, server)

    def shutdown_all_servers(self) -> None:
        self._all_servers_do(lambda r, s: self.shutdown_server(
            r, s["id"]) if "status" in s and s["status"] == "ACTIVE" else None)

    def turn_on_all_servers(self) -> None:
        self._all_servers_do(lambda r, s: self.turn_on_server(
            r, s["id"]) if "status" in s and s["status"] == "SHUTOFF" else None)

    def _send_request(self, method: str, url: str, data: dict = None) -> dict:
        response = requests.request(
            method,
            url,
            headers={
                "Authorization": self.api_key,
            },
            data=json.dumps(data) if data else None,
        )
        if not 200 <= response.status_code < 300:
            raise Exception(response.text)
        if not response.text:
            return {}
        return response.json()
