import pyotp
from datetime import datetime,timedelta
def send_otp(request):
    totp=pyotp.TOTP(pyotp.random_base32(),interval=60)
    otp=totp.now()
    request.session['otp_secret_key']=totp.secret
    valid_date=datetime.now()+timedelta(minutes=1)
    request.session['otp_valid_date']=valid_date

    print((f"Your one time password is {otp}"))
    
def generate_otp():
    """Generate a 6-digit OTP."""
    return random.randint(100000, 999999)
