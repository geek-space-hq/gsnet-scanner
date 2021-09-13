import csv
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
    with open((HERE / ".." / "assets" / "list.csv").resolve()) as f:
        reader = csv.reader(f)
        all_hosts = {row[0]: row[1] == "True" for row in reader}
    if addr not in all_hosts.keys():
        return render_template("check.html", message=f"Host {addr} is not exists")

    message = (
        "Password authentication is enabled!!"
        if True == all_hosts[addr]
        else "Password authentication is disabled"
    )
    return render_template("check.html", message=message)
