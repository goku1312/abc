from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from app import models
import json
from django.http import JsonResponse

from django.contrib import messages
from .models import*
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from gtts import gTTS
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.shortcuts import render, get_object_or_404



# Create your views here.
def index(request):
    # uid=request.session['username']
    doctor_details = DoctorRegister.objects.all()
  
  
    return render(request,"index-2.html", {"doctor_details": doctor_details})


def cart(request):
    return render(request,"cart.html")



def checkout(request):
    return render(request,"checkout.html")



def shop(request):
    return render(request,"shop-list-sidebar.html")


def blog(request):
    return render(request,"blog-grid.html")

def blogdetails(request):
    return render(request,"blog-details.html")


def vendor(request):
    return render(request,"vendor.html")


def contact(request):
    return render(request,"contact-us.html")


def vendorprofile(request):
    return render(request,"vendor-profile.html")


def compare(request):
    return render(request,"compare.html")

def login(request):
    return render(request,"login/signup.html")

def vendordashboard(request):
    return render(request,"vendor-dashboard.html")


def new_page(request):
    return render(request,"login/signup.html")




# def register(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        request.session['emaill'] = email
        phonenumber=request.POST.get("phonenumber")
        password = request.POST.get('password')

        # Check if username already exists
        if Register.objects.filter(username=username).exists():
            error_messages = 'Username already exists.'
            messages.info(request, error_messages)
            return HttpResponseRedirect('login')

       
        # user = Register.objects.create(username=username, email=email,phonenumber=phonenumber ,password=password).save()

            
        message =  get_random_string(length=4, allowed_chars='0123456789')
        request.session['message']=message
            
        
        # Assuming you have a default email address set in your Django settings
        recipient_email = settings.DEFAULT_FROM_EMAIL
      
        print(email)
        print(recipient_email)
       
        # Send email
        send_mail(
    'Send registration email with verification link',
    'Welcome to Our Website - Verify Your Email',
    f'''
Hi {username},

Thank you for registering on our website! Your verification code is: {message}

If you didn't register on our website, please ignore this email.

Regards,
Your Website Team
''',
    settings.DEFAULT_FROM_EMAIL,
    [email],
     
    
)

        # Return a success response
            
        messages.success(request,
                         'Successfully registered! An email has been sent to your email address for verification.')

        return render(request,'otp.html')

        # Render registration form template for GET request
    return render(request, 'login/index12.html')


def register(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get('password')
        request.session['username'] = username
        request.session['email'] = email
        request.session['phonenumber'] = phonenumber
        request.session['password'] = password
        # Check if username already exists
        if Register.objects.filter(email=email).exists():
            error_messages = 'Username already exists.'
            messages.info(request, error_messages)
            return HttpResponseRedirect('login')        
        else:
            return HttpResponseRedirect('otp')    
        # return render(request, 'otp.html')
    # Render registration form template for GET request
    return render(request, 'login/signup.html')



def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        print(email)

        # Check if a user with the provided email and password exists
        user = Register.objects.filter(email=email, password=password).first()
        doctor_details = DoctorRegister.objects.all()

        if user:
            # User exists, set session flag and redirect to the home page or any other desired URL
            request.session['is_logged_in'] = True
            request.session['email'] = email
            request.session['username'] = user.username
            request.session.save()
            return render(request, "index-2.html", {'uid': user.username,"doctor_details":doctor_details})
        else:
            # User does not exist or incorrect credentials provided
            error_message = 'Incorrect Username or password. Please try again.'
            messages.info(request, error_message)
            print(error_message)
            return HttpResponseRedirect('signin')

    return render(request, 'login/signin.html')



def logout(request):
    request.session['is_logged_in']=False
    request.session['is_doclogged_in']=False
    return HttpResponseRedirect('index')




def otp(request):

        username=request.session['username']
        email=request.session['email']
        phonenumber=request.session['phonenumber']
        password=request.session['password']
        message = get_random_string(length=4, allowed_chars='0123456789')
        request.session['message'] = message

        # Assuming you have a default email address set in your Django settings
        recipient_email = settings.DEFAULT_FROM_EMAIL
      
        print(email)
       
        # Send email
        send_mail(
    'OTP Verification',
    f'Hi {username},\n\n'
    f'Thank you for registering on our website! Your One-Time Password (OTP) for verification is: {message}\n\n'
    f'If you didn\'t register on our website, please ignore this email.\n\n'
    f'Regards,\n'
    f'Your Website Team',
    settings.DEFAULT_FROM_EMAIL,
    [email],
    fail_silently=False,
)
        
        # Return a success response
        messages.success(request,
                         'Successfully registered! An email has been sent to your email address for verification.')
        return render(request,"otp.html" ,{"email" : email})








def newlogin(request):
    return render(request,"newlogin.html")




def signin(request):
    return render(request,"login/signin.html")




def verifyotp(request):

    if request.method == 'POST':
        # Get values from the input fields
        otp1 = request.POST.get('otp1', '')
        otp2 = request.POST.get('otp2', '')
        otp3 = request.POST.get('otp3', '')
        otp4 = request.POST.get('otp4', '')
        username=request.session['username']
        email=request.session['email']
        phonenumber=request.session['phonenumber']
        password=request.session['password']

        # Combine the values into one string
        combined_otp = otp1 + otp2 + otp3 + otp4
        message=request.session['message']

        if int(combined_otp) == int(message):
            user = Register.objects.create(username=username, email=email,phonenumber=phonenumber ,password=password).save()
            request.session['is_logged_in']=True
            
            return HttpResponseRedirect('index')
        else:
            messages.error(request, 'Invalid OTP')





def terms(request):
    return render(request,"terms.html")




def plans(request):
    return render(request,"plans.html")




def plans1(request):
    return render(request,"plans1.html")




def doctor(request):
    return render(request,"doctor.html")



def doctorprofile(request):
    if 'email' in request.session:
        email = request.session['email']
        doctor_details = DoctorRegister.objects.filter(email=email).first() 
        patient_details = Register.objects.all()
        details = MedicalRecord.objects.all()
         # Retrieve the first record matching the email
        return render(request, "doctorprofile.html", {"doctor_details": doctor_details,"patient_details":patient_details,"details":details})
  





def doctorlogin(request):
    return render(request,"doctorlogin/signin.html")


def doctorsignin(request):
    return render(request,"doctorlogin/signup.html")






def doctor_login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        print(email)

        # Check if a user with the provided email and password exists
        user = DoctorRegister.objects.filter(email=email, password=password).first()
        # print("1",user.username)

        if user:
            
            # User exists, set session flag and redirect to the home page or any other desired URL
            request.session['is_doclogged_in'] = True
            request.session['email'] = email
            request.session['username'] =user.username
            uid=request.session['username']
            
            request.session.save()
            return HttpResponseRedirect('doctorprofile')
            # return HttpResponseRedirect('index')
        else:
            # User does not exist or incorrect credentials provided
            error_message = 'Incorrect Username or password. Please try again.'
            messages.info(request, error_message)
            print(error_message)
            return HttpResponseRedirect('doctorsignin')

    return render(request, 'doctorlogin/signin.html')
            # User exists, set session flag and redirect to the home page or any other desired URL
       




def docregister(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get('password')
        request.session['username'] = username
        request.session['email'] = email
        request.session['phonenumber'] = phonenumber
        request.session['password'] = password
        # Check if username already exists
        if DoctorRegister.objects.filter(email=email).exists():
            error_messages = 'Email already exists.'
            messages.info(request, error_messages)
            return HttpResponseRedirect('doctorlogin')
        
        else:
            return HttpResponseRedirect('otp1')
        

        # return render(request, 'otp.html')

    # Render registration form template for GET request
    return render(request, 'doctorlogin/signup.html')



def otp1(request):

        username=request.session['username']
        email=request.session['email']
        phonenumber=request.session['phonenumber']
        password=request.session['password']
        message = get_random_string(length=4, allowed_chars='0123456789')
        request.session['message'] = message

        # Assuming you have a default email address set in your Django settings
        recipient_email = settings.DEFAULT_FROM_EMAIL
      
        print(email)
       
        # Send email
        send_mail(
    'OTP Verification',
    f'Hi {username},\n\n'
    f'Thank you for registering on our website! Your One-Time Password (OTP) for verification is: {message}\n\n'
    f'If you didn\'t register on our website, please ignore this email.\n\n'
    f'Regards,\n'
    f'Your Website Team',
    settings.DEFAULT_FROM_EMAIL,
    [email],
    fail_silently=False,
)
        
        # Return a success response
        messages.success(request,
                         'Successfully registered! An email has been sent to your email address for verification.')
        return render(request,"otp1.html" ,{"email" : email})







def verifyotp1(request):

    if request.method == 'POST':
        # Get values from the input fields
        otp1 = request.POST.get('otp1', '')
        otp2 = request.POST.get('otp2', '')
        otp3 = request.POST.get('otp3', '')
        otp4 = request.POST.get('otp4', '')
        username=request.session['username']
        email=request.session['email']
        phonenumber=request.session['phonenumber']
        password=request.session['password']

        # Combine the values into one string
        combined_otp = otp1 + otp2 + otp3 + otp4
        message=request.session['message']

        if int(combined_otp) == int(message):
            user = DoctorRegister.objects.create(username=username, email=email,phonenumber=phonenumber ,password=password).save()
            request.session['is_doclogged_in']=True
            
            return HttpResponseRedirect('doctorprofile')
        else:
            messages.error(request, 'Invalid OTP')




def docprofsave(request):
    if request.method == 'POST':
        # Retrieve form data
        uid=request.session['username']
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        exp = request.POST.get('exp')
        spec = request.POST.get('spec')
        cntry = request.POST.get('cntry')
        email = request.session['email'] 
        desc = request.POST.get('desc') # Assuming the user's email is used as the lookup value
        
        # Retrieve existing record based on user's email
        doc_register = get_object_or_404(DoctorRegister, email=email)
        
        # Compare with existing data and update only if changed
        if doc_register.username != name:
            doc_register.username = name
        if doc_register.phonenumber != contact:
            doc_register.phonenumber = contact
        if doc_register.exp != exp:
            doc_register.exp = exp
        if doc_register.spec != spec:
            doc_register.spec = spec
        if doc_register.cntry != cntry:
            doc_register.cntry = cntry
        if doc_register.desc != desc:
            doc_register.desc = desc

        # Save the changes
        doc_register.save()
        
        return HttpResponseRedirect('doctorprofile')  # Redirect to success page or wherever you want
    else:
        return HttpResponseRedirect('doctorprofile')
    






def numb_otp(request):
    if request.method == 'POST':
        try:
            # Twilio Account SID, Auth Token, and Verify Service SID
            account_sid = "ACc066745b21b04e8212cf13d251537d69"
            auth_token = "8e284fc876454098f9773620902dfdaa"
            verify_sid = "VAf4325c86b54cb521f1d2bcbe1cbd3e21"
            
            # Phone number to send OTP to (in E.164 format)
            verified_number = "+917907334688"
            
            # Initialize Twilio client
            client = Client(account_sid, auth_token)
            
            # Send OTP via SMS
            verification = client.verify.services(verify_sid) \
                .verifications \
                .create(to=verified_number, channel="sms")
            
            # Log verification status
            print(verification.status)
            
            return HttpResponse("OTP sent successfully!")
        
        except TwilioRestException as e:
            # Log the Twilio error and return failure response
            print(e)
            return HttpResponse("Failed to send OTP. Please try again later.")
    
    else:
        return render(request, 'numb_otp.html')

def numbverify_otp(request):
    if request.method == 'POST':
        try:
            # Twilio Account SID, Auth Token, and Verify Service SID
            account_sid = "ACc066745b21b04e8212cf13d251537d69"
            auth_token = "887f15a8342f53c798e6462a06bcfb4c"
            verify_sid = "VAf4325c86b54cb521f1d2bcbe1cbd3e21"
            
            # Phone number to verify OTP against (in E.164 format)
            verified_number = "+917907334688"
            
            # Get OTP code from the request
            otp_code = request.POST.get('otp_code')
            
            # Initialize Twilio client
            client = Client(account_sid, auth_token)
            
            # Verify OTP code
            verification_check = client.verify.services(verify_sid) \
                .verification_checks \
                .create(to=verified_number, code=otp_code)
            
            # Log verification status
            print(verification_check.status)
            
            return HttpResponse("OTP verified successfully!")
        
        except TwilioRestException as e:
            # Log the Twilio error and return failure response
            print(e)
            return HttpResponse("Failed to verify OTP. Please enter a valid OTP.")
    
    else:
        return render(request, 'verify_otp.html')
    



from django.http import JsonResponse

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        email = request.session['email']  # Assuming the user's email is used as the lookup value
        
        # Retrieve existing record based on user's email
        doc_register = get_object_or_404(DoctorRegister, email=email)
        if doc_register.image != image:
            doc_register.image = image
            doc_register.save()
        # doctor = DoctorRegister(image=image)
        # doctor.save()
        
     
        return JsonResponse({'status': 'success'})
     
        
    return JsonResponse({'status': 'error'})

def delete_image(request):
    if request.method == 'POST':
        # Assuming you receive the ID of the image to delete in the request
        image_id = request.POST.get('image_id')
        if image_id:
            # Retrieve the DoctorRegister object by its ID
            doctor = get_object_or_404(DoctorRegister, pk=image_id)
            # Delete the image file from the server (optional, if you want to delete the file physically)
            doctor.image.delete(save=False)  # Assuming 'image' is the field name
            # Delete the DoctorRegister object
            doctor.delete()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})




def patientprofile(request):
    if 'email' in request.session:
        email = request.session['email']
        doctor_details = Register.objects.filter(email=email).first() 
         # Retrieve the first record matching the email
        return render(request, "patientprofile.html", {"doctor_details": doctor_details})







def patprofsave(request):
    if request.method == 'POST':
        # Retrieve form data
        uid=request.session['username']
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        bystander = request.POST.get('bystander')
        bystandercontact = request.POST.get('bystandercontact')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        bp = request.POST.get('bp')
        sugar = request.POST.get('sugar')
        email = request.session['email'] 
        cntry = request.POST.get('cntry') # Assuming the user's email is used as the lookup value
        
        # Retrieve existing record based on user's email
        doc_register = get_object_or_404(Register, email=email)
        
        # Compare with existing data and update only if changed
        if doc_register.username != name:
            doc_register.username = name
        if doc_register.phonenumber != contact:
            doc_register.phonenumber = contact
        if doc_register.bystander != bystander:
            doc_register.bystander= bystander
        if doc_register.bystandercontact != bystandercontact:
            doc_register.bystandercontact = bystandercontact
        if doc_register.cntry != cntry:
            doc_register.cntry = cntry
        if doc_register.height != height:
            doc_register.height = height
        if doc_register.weight != weight:
            doc_register.weight = weight
        if doc_register.bp != bp:
            doc_register.bp = bp
        if doc_register.sugar != sugar:
            doc_register.sugar= sugar

        # Save the changes
        doc_register.save()
        
        return HttpResponseRedirect('patientprofile')  # Redirect to success page or wherever you want
    else:
        return HttpResponseRedirect('patientprofile')    
    




def paupload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        email = request.session['email']  # Assuming the user's email is used as the lookup value
        
        # Retrieve existing record based on user's email
        doc_register = get_object_or_404(Register, email=email)
        if doc_register.image != image:
            doc_register.image = image
            doc_register.save()
        # doctor = DoctorRegister(image=image)
        # doctor.save()
        
     
        return JsonResponse({'status': 'success'})
     
        
    return JsonResponse({'status': 'error'})






def trail(request):
    return render(request,"jhgjhghghjgjh.html")



def kl(request):
    return render(request,"kl.html")





def save_medical_record(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        patient_name = data.get('patientName')
        medicine = data.get('medicine')
        time = data.get('time')
        date = data.get('date')
        allergies = data.get('allergies')

        # Save data to MedicalRecord table
        medical_record = MedicalRecord.objects.create(
            patient_name=patient_name,
            medicine=medicine,
            time=time,
            date=date,
            allergies=allergies
        )

        return JsonResponse({"message": "Medical record saved successfully!"})

    return JsonResponse({"error": "Method not allowed."}, status=405)



from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# def generate_pdf(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         patient_name = data.get('patient_name', '')

#         details = MedicalRecord.objects.filter(patient_name=patient_name)

#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="{patient_name}_medical_record.pdf"'

#         # Create PDF
#         c = canvas.Canvas(response, pagesize=letter)
#         y = 750
#         for detail in details:
#             c.drawString(100, y, f'Patient Name: {detail.patient_name}')
#             c.drawString(100, y - 20, f'Medicine: {detail.medicine}')
#             c.drawString(100, y - 40, f'Time: {detail.time}')
#             c.drawString(100, y - 60, f'Date: {detail.date}')
#             c.drawString(100, y - 80, f'Allergies: {detail.allergies}')
#             y -= 100
#             if y < 50:
#                 c.showPage()
#                 c = canvas.Canvas(response, pagesize=letter)
#                 y = 750
#         c.save()

#         return response
#     else:
#         return HttpResponse(status=400)




# from .models import MedicalRecord
# import json
# from datetime import datetime

# def generate_pdf(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         patient_name = data.get('patient_name', '')

#         details = MedicalRecord.objects.filter(patient_name=patient_name)

#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="{patient_name}_medical_record.pdf"'

#         # Create PDF
#         c = canvas.Canvas(response, pagesize=letter)

#         # Add medical logo
#         # c.drawImage('path_to_medical_logo.png', 50, 750, width=100, height=100)

#         # Add date and time
#         now = datetime.now()
#         current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
#         c.drawString(450, 800, f'Date and Time: {current_date_time}')

#         y = 700
#         for detail in details:
#             c.drawString(100, y, f'Patient Name: {detail.patient_name}')
#             c.drawString(100, y - 20, f'Medicine: {detail.medicine}')
#             c.drawString(100, y - 40, f'Time: {detail.time}')
#             c.drawString(100, y - 60, f'Date: {detail.date}')
#             c.drawString(100, y - 80, f'Allergies: {detail.allergies}')
#             y -= 100
#             if y < 50:
#                 c.showPage()
#                 c = canvas.Canvas(response, pagesize=letter)
#                 # Add medical logo on subsequent pages if needed
#                 c.drawImage('path_to_medical_logo.png', 50, 750, width=100, height=100)
#                 # Add date and time on subsequent pages if needed
#                 c.drawString(450, 800, f'Date and Time: {current_date_time}')
#                 y = 750

#         # Add signature
#         c.drawString(100, 50, "Signature:")
#         c.line(200, 40, 400, 40)

#         c.save()

#         return response
#     else:
#         return HttpResponse(status=400)






from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
import os
from xhtml2pdf import pisa

def generate_pdf(request):
    # Define the path to your HTML template
    template_path = os.path.join(settings.BASE_DIR, 'app', 'templates', 'kl.html')

    # Render the HTML template
    template = get_template(template_path)
    context = {}  
    html = template.render(context)

    # Define the path to save the PDF file
    pdf_path = os.path.join(settings.BASE_DIR, 'app', 'templates', 'kl.pdf')

    # Generate PDF using xhtml2pdf
    with open(pdf_path, 'wb') as pdf_file:
        pisa.CreatePDF(html, dest=pdf_file)

    # Read the content of the generated PDF file
    with open(pdf_path, 'rb') as pdf_file:
        pdf_content = pdf_file.read()

    # Prepare the HTTP response with PDF content
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="kl.pdf"'

    return response





def form(request):
    return render(request,"lll.html")




def doctor_list(request):
    return render(request,"doctor_list.html")



def book(request):
    doctor_details = DoctorRegister.objects.all()
    return render(request,"booking.html",{"doctor_details": doctor_details})



def comment(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('commentt', '')

        # Assuming you have a default email address set in your Django settings
        recipient_email = settings.DEFAULT_FROM_EMAIL
        print(name)
        print(email)
        print(message)
        print(recipient_email)
        # Send email
        send_mail(
            'New Form Submission',
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            email,
            [recipient_email],
            fail_silently=False,
        )

        # Return a success response
        return HttpResponseRedirect("contact")

    return HttpResponseRedirect('contact')




def doctorbook(request):
    return render(request,"product-detail-2.html")