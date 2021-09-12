import csv
from gsnet_scanner.scanner import check_password_login, list_hosts, list_opened_ports
import pathlib

from flask import render_template, request

from gsnet_scanner import app

HERE = pathlib.Path(__file__).parent.resolve()


@app.route("/hosts", methods=["GET"])
def hosts():
    with open((HERE / ".." / "assets" / "list.csv").resolve()) as f:
        reader = csv.reader(f)
        return render_template("hosts.html", hosts_list=reader)


@app.route("/check", methods=["GET"])
def check():
    q_strings = request.args.copy()
    if not q_strings.get("addr"):
        return 400
    addr = q_strings["addr"]
    if q_strings["addr"] not in list_hosts():
        return render_template("check.html", message=f"Host {addr} is not exists")

    password_login_all_ports = set()
    for port in list_opened_ports(addr):
        password_login_all_ports.add(check_password_login(addr, str(port)))
    message = (
        "Passowrd authentication is enabled!!"
        if True in password_login_all_ports
        else "Passowrd authentication is disabled"
    )
    return render_template("check.html", message=message)
