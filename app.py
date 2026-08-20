import os
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "change-this-secret")

VERIFY_PASSWORD = os.environ.get("VERIFY_PASSWORD", "7870778171")

EMPLOYEE = {
    "name": "Nisha Kumari",
    "id": "EMP130820",
    "designation": "Data Entry Executive",
    "department": "Data Operations",
    "joining_date": "20 August 2026",
    "work_mode": "Remote",
    "status": "Active",
}

@app.route("/")
def home():
    return redirect(url_for("verify"))

@app.route("/verify/<employee_id>", methods=["GET", "POST"])
def verify(employee_id):
    if employee_id != EMPLOYEE["id"]:
        return render_template("invalid.html"), 404

    error = None
    verified = session.get("verified_employee") == employee_id

    if request.method == "POST":
        password = request.form.get("password", "")
        if password == VERIFY_PASSWORD:
            session["verified_employee"] = employee_id
            return redirect(url_for("verify", employee_id=employee_id))
        error = "Invalid verification password."
        verified = False

    return render_template(
        "verify.html",
        employee=EMPLOYEE,
        verified=verified,
        error=error
    )

@app.route("/logout")
def logout():
    session.pop("verified_employee", None)
    return redirect(url_for("verify", employee_id=EMPLOYEE["id"]))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
