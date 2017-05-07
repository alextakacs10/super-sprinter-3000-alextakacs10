from flask import Flask, request, render_template, url_for, redirect
import random

app = Flask(__name__)


def importdata():
    with open("data.csv", "r", encoding="utf-8") as datafile:
        entries = datafile.readlines()
        entries = [entry.replace("\n", "").split(";") for entry in entries]
    return entries


@app.route("/list")
@app.route("/")
def index():
    entries = importdata()
    columns = ["ID", "Story title", "User story", "Acceptance Criteria", "Business value", "Estimation", "Status"]
    return render_template("list.html", columns=columns, entries=entries)


@app.route("/story")
def story():
    title = "Add new story"
    return render_template("form.html", title=title)


@app.route("/savedata/", methods=["POST"])
def savedata():
    id_number = len(importdata()) + 1
    st_title = request.form["st_title"]
    usr_story = request.form["usr_story"]
    acc_crit = request.form["acc_crit"]
    bus_val = request.form["bus_val"]
    estimation_h = request.form["estimation_h"]
    status = request.form["status"]
    with open("data.csv", "a", encoding="utf-8") as datafile:
        datafile.writelines(";".join([str(id_number), st_title, usr_story, acc_crit, bus_val, estimation_h, status + "\n"]))
    return redirect("/list")


@app.route("/story/<id_number>")
def edit_story(id_number):
    title = "Edit"
    entries = importdata()
    entry_needed = entries[int(id_number) - 1]
    return render_template("form.html", entry_needed=entry_needed, title=title, id_number=id_number)


@app.route("/updatedata/", methods=["POST"])
def updatedata():
    id_number = 2
    st_title = request.form["st_title"]
    usr_story = request.form["usr_story"]
    acc_crit = request.form["acc_crit"]
    bus_val = request.form["bus_val"]
    estimation_h = request.form["estimation_h"]
    status = request.form["status"]

    updated_entry = [str(id_number), st_title, usr_story, acc_crit, bus_val, estimation_h, status + "\n"]
    entries = importdata()
    new_entries = entries
    for entry in new_entries:
        if entry[0] == updated_entry[0]:
            entry = updated_entry

    with open("data.csv", "w", encoding="utf-8") as datafile:
        for entry in new_entries:
            datafile.write(";".join(entry) + "\n")
    return redirect("/list")


if __name__ == "__main__":
    app.run(debug=True)