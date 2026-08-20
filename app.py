import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for
)

app = Flask(__name__)


# =========================================================
# SECURITY CONFIGURATION
# =========================================================

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

# Session lifetime: 5 minutes
app.permanent_session_lifetime = timedelta(minutes=5)

# Secure browser session settings
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="Lax"
)


# =========================================================
# INDIA TIMEZONE
# =========================================================

INDIA_TZ = ZoneInfo("Asia/Kolkata")


# =========================================================
# EMPLOYEE RECORD
# =========================================================

EMPLOYEE = {
    "name": "Nisha Kumari",
    "id": "EMP130820",
    "designation": "Data Entry Executive",
    "department": "Data Operations",
    "joining_date": "20 August 2026",
    "work_mode": "Remote",
    "status": "Active",
}


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return redirect(
        url_for(
            "verify",
            employee_id=EMPLOYEE["id"]
        )
    )


# =========================================================
# EMPLOYEE VERIFICATION
# =========================================================

@app.route("/verify/<employee_id>", methods=["GET", "POST"])
def verify(employee_id):

    # Validate employee ID
    if employee_id != EMPLOYEE["id"]:
        return render_template("invalid.html"), 404

    error = None

    # -----------------------------------------------------
    # CHECK SESSION
    # -----------------------------------------------------

    verified = (
        session.get("verified_employee") == employee_id
    )

    # -----------------------------------------------------
    # PASSWORD VERIFICATION
    # -----------------------------------------------------

    if request.method == "POST":

        password = request.form.get(
            "password",
            ""
        )

        if password == VERIFY_PASSWORD:

            # Make session temporary
            session.permanent = True

            # Store verified employee
            session["verified_employee"] = employee_id

            # Store verification time in IST
            verified_time = datetime.now(INDIA_TZ)

            session["verification_time"] = (
                verified_time.strftime(
                    "%d %B %Y, %I:%M:%S %p IST"
                )
            )

            return redirect(
                url_for(
                    "verify",
                    employee_id=employee_id
                )
            )

        error = "Invalid verification password."
        verified = False

    # -----------------------------------------------------
    # VERIFICATION TIME
    # -----------------------------------------------------

    verification_time = session.get(
        "verification_time"
    )

    return render_template(
        "verify.html",
        employee=EMPLOYEE,
        verified=verified,
        error=error,
        verification_time=verification_time
    )


# =========================================================
# LOCK RECORD
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for(
            "verify",
            employee_id=EMPLOYEE["id"]
        )
    )


# =========================================================
# HEALTH CHECK FOR RENDER
# =========================================================

@app.route("/health")
def health():

    return {
        "status": "ok",
        "service": "Nexora Employee Verification",
        "timezone": "Asia/Kolkata"
    }, 200


# =========================================================
# RUN APPLICATION
# =========================================================

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

           
