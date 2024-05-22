from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
urlpatterns = [
   
    path('',views.index),
    path('index',views.index),
    path('cart',views.cart),
    path('checkout',views.checkout),
    path("shop",views.shop),
    path("blog",views.blog),
    path("blogdetails",views.blogdetails),
    path("vendor",views.vendor),
    path("contact",views.contact),
    path("vendorprofile",views.vendorprofile),
    path("compare",views.compare),
    path("login",views.login),
    path("vendordashboard",views.vendordashboard),
    path("register",views.register),
    path("user_login",views.user_login),
    path("logout",views.logout),
    path("new_page",views.new_page),
    path("otp",views.otp),
    # path("resent",views.resent),
    path("newlogin",views.newlogin),
    path("signin",views.signin),
    path("verifyotp",views.verifyotp),
    path("terms",views.terms),
    path("plans",views.plans),
    path("plans1",views.plans1),
    path("doctor",views.doctor),
    path("doctorprofile",views.doctorprofile),
    path("doctorlogin",views.doctorlogin),
      path("doctorsignin",views.doctorsignin),
      path("doctor_login",views.doctor_login),
      path("docregister",views.docregister),
      path('otp1',views.otp1),
      path('verifyotp1',views.verifyotp1),
      path("docprofsave",views.docprofsave),
      path('numb_otp',views.numb_otp),
      path("numbverify_otp",views.numbverify_otp),
         path('upload_image',views.upload_image),
         path('paupload_image',views.paupload_image),
    path('delete_image',views.delete_image),
    path('patientprofile',views.patientprofile),
    path('patprofsave',views.patprofsave),
    path('trail',views.trail),
    path('kl',views.kl),
     path('save-medical-record/', views.save_medical_record, name='save_medical_record'),
     path('generate_pdf', views.generate_pdf, name='generate_pdf'),
     path('form',views.form),
     path('doctor_list',views.doctor_list),
     path('book',views.book),
     path('comment',views.comment),

     path('doctorbook',views.doctorbook),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)