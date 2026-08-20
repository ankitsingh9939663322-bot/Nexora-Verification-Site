import os
from datetime import timedelta

from flask import Flask, render_template, request, session, redirect, url_for


app = Flask(__name__)


# ============================================================
# SECURITY CONFIGURATION
# ============================================================

SESSION_SECRET = os.environ.get("SESSION_SECRET")
VERIFY_PASSWORD = os.environ.get("VERIFY_PASSWORD")

if not SESSION_SECRET:
    raise RuntimeError(
        "SESSION_SECRET environment variable is not configured."
    )

if not VERIFY_PASSWORD:
    raise RuntimeError(
        "VERIFY_PASSWORD environment variable is not configured."
    )

app.secret_key = SESSION_SECRET

# Verification session expires after 5 minutes.
app.permanent_session_lifetime = timedelta(minutes=5)


# ============================================================
# EMPLOYEE RECORD
# ============================================================

EMPLOYEE = {
    "name": "Nisha Kumari",
    "id": "EMP130820",
    "designation": "Data Entry Executive",
    "department": "Data Operations",
    "joining_date": "20 August 2026",
    "work_mode": "Remote",
    "status": "Active",
}


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return redirect(
        url_for(
            "verify",
            employee_id=EMPLOYEE["id"]
        )
    )


# ============================================================
# EMPLOYEE VERIFICATION
# ============================================================

@app.route("/verify/<employee_id>", methods=["GET", "POST"])
def verify(employee_id):

    # Only the registered employee record can be accessed.
    if employee_id != EMPLOYEE["id"]:
        return render_template("invalid.html"), 404

    error = None

    # Check current verification session.
    verified = (
        session.get("verified_employee") == employee_id
    )

    if request.method == "POST":

        password = request.form.get(
            "password",
            ""
        ).strip()

        if password == VERIFY_PASSWORD:

            # Make the session temporary.
            session.permanent = True

            # Store verified employee.
            session["verified_employee"] = employee_id

            # Redirect after successful verification.
            return redirect(
                url_for(
                    "verify",
                    employee_id=employee_id
                )
            )

        error = "Invalid verification password."
        verified = False

    return render_template(
        "verify.html",
        employee=EMPLOYEE,
        verified=verified,
        error=error,
        verification_time=None
    )


# ============================================================
# MANUAL LOCK
# ============================================================

@app.route("/logout")
def logout():

    # Completely remove the verification session.
    session.clear()

    return redirect(
        url_for(
            "verify",
            employee_id=EMPLOYEE["id"]
        )
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return {
        "status": "ok",
        "service": "Nexora Employee Verification"
    }, 200


# ============================================================
# LOCAL DEVELOPMENT
# ============================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )


