import re
import random
import string
import json
import uuid
from datetime import datetime, timedelta
import pyotp

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.files.storage import default_storage
from django.core.mail import send_mail

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Voter, Profile, SetPassword
from .models import Candidate  # Ensure this import is correct
from .forms import SetPasswordForm
from .helpers import send_forget_password_mail
from .util import send_otp, generate_otp

from .models import SetPassword  # Make sure this import is correct
# **Unique ID Generator**
def generate_unique_id():
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    numbers = ''.join(random.choices(string.digits, k=6))
    return letters + numbers


# **Password Validation**
def validate_password(password):
    return bool(re.fullmatch(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password))




# **Serializer for Voter**
class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ["full_name", "email", "phone", "dob", "sex", "id_type", "id_number", "id_doc", "photo", "password"]

    def create(self, validated_data):
        validated_data["unique_id"] = generate_unique_id()
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


# **Register Voter API**
@csrf_exempt
def register_view(request):
    if request.method == "POST":
        try:
            data = request.POST
            files = request.FILES

            full_name = data.get("fullName", "").strip()
            email = data.get("email", "").strip()
            phone = data.get("phone", "").strip()
            dob_str = data.get("dateOfBirth", "").strip()
            sex = data.get("sex", "").strip()
            address = data.get("address", "").strip()
            id_type = data.get("identificationType", "").strip()
            id_number = data.get("identificationNumber", "").strip()
            id_doc = files.get("id_doc")
            photo = files.get("photo")
            consent = data.get("consent", "false").lower() == "true"

            # **Validations**
            if not all([full_name, email, phone, dob_str, sex, address, id_type, id_number, id_doc, photo]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            if Voter.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already registered"}, status=400)
            if Voter.objects.filter(phone=phone).exists():
                return JsonResponse({"error": "Phone number already registered"}, status=400)

            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            if dob.year > 2006:
                return JsonResponse({"error": "You must be at least 18 years old"}, status=400)

            if id_type == "Aadhar Card" and not (len(id_number) == 12 and id_number.isdigit()):
                return JsonResponse({"error": "Aadhar Card must have 12 digits"}, status=400)
            if id_type == "Voter Id" and not re.match(r"^[A-Z]{3}[0-9]{7}$", id_number):
                return JsonResponse({"error": "Voter ID must start with 3 uppercase letters followed by 7 digits"}, status=400)

            # **Create Voter Record**
            unique_id = generate_unique_id()
            voter = Voter.objects.create(
                full_name=full_name, email=email, phone=phone, dob=dob, sex=sex, address=address,
                id_type=id_type, id_number=id_number, id_doc=id_doc, photo=photo,
                unique_id=unique_id, consent=consent
            )
            voter.save()

            return JsonResponse({"message": "Registration successful!", "unique_id": voter.unique_id}, status=201)

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

        return JsonResponse({"error": "Invalid request method"}, status=405)

    return render(request, 'register.html')

def send_otp(phone_number, otp):
    """Send OTP to the user's phone number using an SMS gateway."""
    # Replace this with actual SMS gateway integration
    print(f"Sending OTP {otp} to phone number {phone_number}")
    # Example: Use Twilio, Nexmo, or any SMS API here
    # twilio_client.messages.create(
    #     body=f"Your OTP is {otp}",
    #     from_="+1234567890",  # Replace with your Twilio number
    #     to=phone_number
    # )
    return True

# **OTP Verification & Login**
@csrf_exempt
def otp(request):
    error_message = None
    if request.method == "POST":
        otp = request.POST['otp']
        unique_id = request.session.get('unique_id')

        otp_secret_key = request.session.get('otp_secret_key')
        otp_valid_until = request.session.get('otp_valid_until')

        if otp_secret_key and otp_valid_until:
            valid_until = datetime.fromisoformat(otp_valid_until)
            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    user = get_object_or_404(Voter, unique_id=unique_id)
                    login(request, user)
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_until']
                    return redirect('/api/dashboard/')
                else:
                    error_message = "Invalid OTP"
            else:
                error_message = "OTP has expired"
        else:
            error_message = "OTP not found"

    return render(request, 'otp.html', {'error_message': error_message})
from .util import generate_otp, send_otp

@csrf_exempt
def send_otp_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone_number = data.get("phone")

            if not phone_number:
                return JsonResponse({"error": "Phone number is required"}, status=400)

            # Generate OTP
            otp = generate_otp()

            # Save OTP and expiration time in session
            request.session["otp"] = otp
            request.session["otp_valid_until"] = (datetime.now() + timedelta(minutes=5)).isoformat()

            # Send OTP to the phone number
            if send_otp(phone_number, otp):
                return JsonResponse({"message": "OTP sent successfully"}, status=200)
            else:
                return JsonResponse({"error": "Failed to send OTP"}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def home(request):
    return render(request, 'home.html')


# **Upload Photo**
@csrf_exempt
def upload_photo(request, unique_id):
    if request.method == 'POST' and request.FILES.get('photo'):
        photo = request.FILES['photo']
        file_path = default_storage.save(f'images/{unique_id}_{photo.name}', photo)
        file_url = request.build_absolute_uri(settings.MEDIA_URL + file_path)
        return JsonResponse({'file_url': file_url}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)


# **Upload ID Document**
@csrf_exempt
def upload_id_document(request, unique_id):
    if request.method == "POST" and request.FILES.get("id_doc"):
        id_doc = request.FILES["id_doc"]
        file_path = default_storage.save(f'documents/{unique_id}_{id_doc.name}', id_doc)
        file_url = request.build_absolute_uri(settings.MEDIA_URL + file_path)
        return JsonResponse({"message": "ID document uploaded successfully", "file_url": file_url})
    return JsonResponse({"error": "Invalid request"}, status=400)
import logging

logger = logging.getLogger(__name__)

# **Password Validation**
def validate_password(password):
    return bool(re.fullmatch(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password))

@csrf_exempt
def set_password(request, unique_id):
    if request.method == "GET":
        return render(request, 'setpassword.html', {'unique_id': unique_id})

    if request.method == "POST":
        password = request.POST.get("password")
        if not password:
            return JsonResponse({"error": "Password is required"}, status=400)

        if not validate_password(password):
            return JsonResponse({
                "error": "Password must be at least 8 characters long and include uppercase, lowercase, number, and special character."
            }, status=400)

        try:
            set_password_entry = SetPassword.objects.create(
                unique_id=unique_id,
                password=make_password(password)
            )
            set_password_entry.save()
            return JsonResponse({"message": "Password successfully updated"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SetPassword, Voter
from datetime import datetime
import json

@csrf_exempt
def login_voter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            unique_id = data.get('unique_id')
            password = data.get('password')

            if not unique_id or not password:
                return JsonResponse({'error': 'Please provide both unique ID and password'}, status=400)

            try:
                user = SetPassword.objects.get(unique_id=unique_id)
            except SetPassword.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

            if check_password(password, user.password):
                try:
                    voter = Voter.objects.get(unique_id=unique_id)
                except Voter.DoesNotExist:
                    return JsonResponse({'error': 'Voter details not found'}, status=404)

                # Calculate age
                today = datetime.today().date()
                age = today.year - voter.dob.year - ((today.month, today.day) < (voter.dob.month, voter.dob.day))

                # Store user data in session
                request.session['user_data'] = {
                    'unique_id': voter.unique_id,
                    'name': voter.full_name,
                    'age': age,
                    'email': voter.email,
                    'phone': voter.phone,
                    'photo': voter.photo.url if voter.photo else ''
                }

                return JsonResponse({'message': 'Login successful', 'redirect_url': '/api/dashboard/'})
            else:
                print("Password validation failed")
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    elif request.method == 'GET':
        return render(request, 'login.html')

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def dashboard_view(request):
    user_data = request.session.get('user_data')
    if not user_data:
        return redirect('/login/')  # Redirect to login if user data is not in session
    return render(request, 'dashboard.html', {'user': user_data})

from django.http import JsonResponse
from .models import Voter

def voters_list_api(request):
    voters = Voter.objects.all().values('unique_id', 'full_name', 'photo', 'email', 'phone')
    for voter in voters:
        voter['photo'] = request.build_absolute_uri(voter['photo']) if voter['photo'] else None
    return JsonResponse(list(voters), safe=False)

def Logout(request):
    logout(request)
    return redirect('/')

def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

def ChangePassword(request, token):
    return render(request, 'changepass.html')


def ForgetPassword(request):
    return render(request, 'forgot.html')

def voters_list_view(request):
    return render(request, 'voterslist.html')

def candidates_list_view(request):
    candidates = Candidate.objects.all()  # Fetch all candidates from the database
    return render(request, 'candidates_list.html', {'candidates': candidates})

def cast_vote_view(request):
    return render(request, 'cast_vote.html')

def results_view(request):
    return render(request, 'results.html')

def edit_details_view(request):
    return render(request, 'edit_details.html')

def polls_view(request):
    return render(request, 'polls.html')

def get_candidates(request):
    candidates = Candidate.objects.all().values("id", "name", "photo", "symbol")
    return JsonResponse(list(candidates), safe=False)

@csrf_exempt
def submit_vote(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            candidate_id = data.get("candidateId")
            # Process the vote (e.g., save to database)
            return JsonResponse({"message": "Vote submitted successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=405)

from django.shortcuts import render

def voting_success(request):
    return render(request, 'voting_success.html')