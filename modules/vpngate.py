from typing import TypedDict

from flask import Blueprint, jsonify
import requests


class VPNItem(TypedDict):
    hostname: str
    country: str
    ip: str
    ping: int
    speed: int


class Module:
    scope = "vpngate"

    def __init__(self, router: Blueprint) -> None:
        router.get("/")(self.api)

    def api(self):
        vpns: list[VPNItem] = []

        resp = requests.get(url="https://www.vpngate.net/api/iphone", stream=True)
        for raw_line in resp.iter_lines():
            if raw_line:
                line = raw_line.decode("utf-8")
                if line.startswith(("*", "#")):
                    continue

                parts = line.split(",")

                try:
                    ping = int(parts[3])
                except:
                    ping = 999999

                try:
                    speed = int(parts[4])
                except:
                    speed = 0

                vpns.append(
                    {
                        "hostname": parts[0],
                        "country": parts[6],
                        "ip": parts[1],
                        "ping": ping,
                        "speed": speed,
                    }
                )

        vpns.sort(key=lambda x: x["speed"] / (x["ping"] + 10), reverse=True)
        return jsonify(vpns)
