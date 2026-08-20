# Nexora Data Solution — Employee Verification

This is a server-side password-protected verification page for employee ID `EMP130820`.

## Current flow
QR scan -> `/verify/EMP130820` -> password -> verified employee details.

## Important
- The password is checked server-side.
- The password is not printed on the ID card.
- Before production deployment, set `VERIFY_PASSWORD` and `SESSION_SECRET` as environment variables.
- After the public domain is available, the QR code should point to:
  `https://YOUR-DOMAIN/verify/EMP130820`
- Only after that URL is tested on a phone should the final ID-card PDF be produced.

## Run locally
```bash
pip install -r requirements.txt
python app.py
```

Then open:
`http://127.0.0.1:5000/verify/EMP130820`
