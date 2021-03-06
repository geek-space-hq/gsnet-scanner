import csv
import pathlib

from flask import abort, render_template, request

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
        return abort(400)
    addr = q_strings["addr"]
    with open((HERE / ".." / "assets" / "list.csv").resolve()) as f:
        reader = csv.reader(f)
        all_hosts = {row[0]: row[1] == "True" for row in reader}
    if addr not in all_hosts.keys():
        return abort(404)

    if True == all_hosts[addr]:  # Password authentication is enabled
        context = {
            "bg_color": "#ffd600",
            "ogp": "enabled.png",
            "title": f"Host {addr} password authentication is enabled!!",
        }
    else:  # Disabled
        context = {
            "bg_color": "#00c853",
            "ogp": "disabled.png",
            "title": f"Host {addr} password authentication is disabled.",
        }
    return render_template("check.html", **context)
