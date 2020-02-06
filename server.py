import os
import json
import time
from flask import Flask, render_template, request, redirect, url_for
from util import valid_course_id, read_excel, list_output

if not os.path.exists("templates"):
    os.mkdir("templates")

app = Flask(__name__)
token_json = json.load(open("token/token.json", "r"))


def token_check(token, default_message):
    if token is None:
        return "invalid token error"

    user = token_json.get(token)
    if user is None:
        return "user not found error"

    return default_message


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "GET":
        token = request.args.get("token")
        message = token_check(token, "submit")
        if message is not "submit":
            return render_template("error.html", error_message=message)
        return render_template("submit.html")
    else:
        token = request.form.get("token")
        message = token_check(token, "valid")
        if message is not "valid":
            return f"""{{"status": "error", "message": "{message}"}}"""

        course_id = request.form.get("course_id")
        if course_id is None or not valid_course_id(course_id):
            return """{{"status": "error", "message": "invalid course id"}}"""

        f = request.files[next(request.files.keys())]
        if f.filename is not "test.xlsx":
            return """{{"status": "error", "message": "invalid file name"}}"""

        input_path = f"input/{token}/course_{course_id}"
        os.makedirs(input_path, exist_ok=True)
        if os.path.exists(f"{input_path}/text.xlsx"):
            timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))
            os.rename(input_path, f"{input_path[:-5]}-{timestamp}.xlsx")
        f.save(input_path)
        _, row_count = read_excel(token, course_id)
        os.system(f"touch state/start_{token}_{course_id}_{row_count}")

        return redirect(url_for("export", token=token, course_id=course_id))


@app.route("/export", methods=["GET"])
def export():
    token = request.args.get("token")
    message = token_check(token, "export")
    if message is not "export":
        return render_template("error.html", error_message=message)

    course_id = request.args.get("course_id")
    if course_id is None or not valid_course_id(course_id):
        return """{{"status": "error", "message": "invalid course id"}}"""

    pdf_list = list_output(token, course_id)

    return render_template("export.html", pdf_list=pdf_list)


if __name__ == "__main__":
    app.run(port=8080)
