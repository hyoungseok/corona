import os
import time
from flask import Flask, render_template, request, redirect, url_for, send_file
from util import valid_token, read_excel, list_output, valid_file_name

if not os.path.exists("templates"):
    os.mkdir("templates")

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "GET":
        token = request.args.get("token")
        if token is None or not valid_token(token):
            return render_template("error.html", error_message="invalid token error")

        return render_template("submit.html", token=token)
    else:
        token = request.form.get("token")
        if token is None or not valid_token(token):
            return render_template("error.html", error_message="invalid token error")

        f = request.files["test"]
        if f.filename != "test.xlsx":
            return render_template("error.html", error_message="invalid file name error")

        input_path = f"input/{token}"
        os.makedirs(input_path, exist_ok=True)
        if os.path.exists(f"{input_path}/test.xlsx"):
            timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))
            os.rename(f"{input_path}/test.xlsx", f"{input_path}/test-{timestamp}.xlsx")
        f.save(f"{input_path}/test.xlsx")
        os.system(f"touch state/start_{token}")

        return redirect(url_for("export", token=token))


@app.route("/export", methods=["GET"])
def export():
    token = request.args.get("token")
    if token is None or not valid_token(token):
        return render_template("error.html", error_message="invalid token error")

    _, total_count = read_excel(token)
    pdf_list = list_output(token)
    pdf_count = len(pdf_list)

    file_name = request.args.get("file_name")
    if file_name is None or not valid_file_name(file_name, token):
        return render_template(
            "export.html",
            total_count=total_count,
            pdf_list=pdf_list,
            pdf_count=pdf_count,
            token=token,
        )

    return send_file(f"output/{token}/{file_name}", as_attachment=True)


if __name__ == "__main__":
    app.run(port=8080)
