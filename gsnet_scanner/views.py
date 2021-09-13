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

    if True == all_hosts[addr]:  # Password authentication is enabled
        context = {
            "hostname": addr,
            "bg_color": "#ffd600",
            "ogp": "enabled.png",
            "status": "password authentication is enabled!!",
        }
    else:  # Disabled
        context = {
            "hostname": addr,
            "bg_color": "#00c853",
            "ogp": "disabled.png",
            "status": "password authentication is disabled.",
        }
    return render_template("check.html", **context)
