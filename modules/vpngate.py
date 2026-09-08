from flask import Blueprint, jsonify
import requests


class Module:
    scope = "vpngate"

    def __init__(self, router: Blueprint) -> None:
        router.get("/")(self.vpngate)

    def vpngate(self):
        vpns: list[dict[str, str]] = []

        resp = requests.get(url="https://www.vpngate.net/api/iphone", stream=True)
        for raw_line in resp.iter_lines():
            if raw_line:
                line = raw_line.decode("utf-8")
                if not line.startswith("public-vpn-"):
                    continue

                parts = line.split(",")
                vpns.append(
                    {
                        "name": parts[0],
                        "addr": parts[1],
                    }
                )

        return jsonify(vpns)
