import os
from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime, timezone

app = Flask(__name__)

# Security configuration
SESSION_SECRET = os.environ.get("SESSION_SECRET")
VERIFY_PASSWORD = os.environ.get("VERIFY_PASSWORD")

# Require secrets to be configured in the deployment environment.
if not SESSION_SECRET:
    raise RuntimeError("SESSION_SECRET environment variable is not configured.")

if not VERIFY_PASSWORD:
    raise RuntimeError("VERIFY_PASSWORD environment variable is not configured.")

app.secret_key = SESSION_SECRET

# Browser-session security
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_PERMANENT=False
)

# Employee record
EMPLOYEE = {
    "name": "Nisha Kumari",
    "id": "EMP130820",
    "designation": "Data Entry Executive",
    "department": "Data Operations",
    "joining_date": "20 August 2026",
    "work_mode": "Remote",
    "status": "Active",
}


@app.route("/health")
def health():
    return {"status": "ok"}, 200


@app.route("/")
def home():
    return redirect(url_for("verify", employee_id=EMPLOYEE["id"]))


@app.route("/verify/<employee_id>", methods=["GET", "POST"])
def verify(employee_id):

    # Check whether the requested employee record exists.
    if employee_id != EMPLOYEE["id"]:
        return render_template("invalid.html"), 404

    error = None
    verification_time = None

    # Check current browser session.
    verified = session.get("verified_employee") == employee_id

    if request.method == "POST":

        password = request.form.get("password", "")

        if password == VERIFY_PASSWORD:
            session["verified_employee"] = employee_id
            session["verified_at"] = datetime.now(
                timezone.utc
            ).strftime("%d %B %Y, %H:%M UTC")

            return redirect(
                url_for("verify", employee_id=employee_id)
            )

        error = "Invalid verification password."
        verified = False

    if verified:
        verification_time = session.get("verified_at")

    return render_template(
        "verify.html",
        employee=EMPLOYEE,
        verified=verified,
        error=error,
        verification_time=verification_time
    )


@app.route("/logout")
def logout():

    # Manually lock the verified record.
    session.pop("verified_employee", None)
    session.pop("verified_at", None)

    return redirect(
        url_for(
            "verify",
            employee_id=EMPLOYEE["id"]
        )
    )


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
