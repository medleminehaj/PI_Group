from flask import Flask, render_template, request, redirect, url_for
import smtplib
import random

app = Flask(__name__)

# Configuration for email sending
EMAIL_ADDRESS = "medleminehaj@gmail.com"
EMAIL_PASSWORD = "amre ztkp xusa zbwo"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Generate a random code for verification
def generate_verification_code():
    return str(random.randint(100000, 999999))

# Send verification email
def send_verification_email(to_email, verification_code):
    subject = "Verification Code"
    body = f"Your verification code is: {verification_code}"
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(EMAIL_ADDRESS, to_email, message)


verification_code = generate_verification_code()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    email = request.form.get('email')
    send_verification_email(email, verification_code)
    return render_template('verify.html', email=email)

@app.route('/success', methods=['POST'])
def success():
    code = request.form.get('code')
    if code == verification_code :
        return render_template('verify.html', erreur="Yes this is the correct code" )
    else :
        return render_template('verify.html', erreur="No this is not the correct code" )

if __name__ == '__main__':
    app.run(debug=True)
