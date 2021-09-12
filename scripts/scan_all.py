from __future__ import annotations
from collections.abc import Iterable
import csv
from io import StringIO
import pathlib
import socket
import subprocess
import urllib.request


HERE = pathlib.Path(__file__).parent.resolve()


REGISTERD_PORTS = (22,) + tuple(range(1024, 49151))
HOSTS_CSV = "https://scrapbox.io/api/table/Geek-SpaceBox/GSNet%E3%81%AE%E3%83%9B%E3%82%B9%E3%83%88%E4%B8%80%E8%A6%A7/hosts.csv"  # noqa


def list_opened_ports(addr: str) -> Iterable[int]:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        for port in REGISTERD_PORTS:
            if not sock.connect_ex((addr, port)):  # port is available
                yield port


def list_hosts() -> Iterable[str]:
    with urllib.request.urlopen(HOSTS_CSV) as f:
        reader = csv.DictReader(StringIO(f.read().decode("UTF-8")))
        for row in reader:
            yield row["IPアドレス"].lstrip("[").rstrip("]")


def check_password_login(addr: str, port: str) -> bool:
    try:
        subprocess.run(
            ["ssh", "-o", "StrictHostKeyChecking=no", "-p", port, addr],
            timeout=1,
            capture_output=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.TimeoutExpired:  # password authentication is enabled
        return True
    else:  # password authentication is disabled
        return False


def main() -> None:
    hosts_list = []
    for addr in list_hosts():
        for port in (ports := list(list_opened_ports(addr))):
            hosts_list.append((addr, check_password_login(addr, str(port))))
        else:
            if not len(ports):
                hosts_list.append((addr, False))
    with open((HERE / ".." / "assets" / "list.csv").resolve(), "w") as f:
        writer = csv.writer(f)
        writer.writerows(hosts_list)


if __name__ == "__main__":
    main()
