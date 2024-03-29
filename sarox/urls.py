from django.urls import path
from .views import UserSignIN,UserLogIn,AdminSignIN,AdminLogIn,AdminLogOut,UserLogOut,Imageupload,UserDetails,User_profile_update
# from django.conf import settings
# from django.conf.urls.static import static


urlpatterns = [

    path('user/reg',UserSignIN.as_view()),
    path('user/login',UserLogIn.as_view()),
    path('user/logout',UserLogOut.as_view()),
    path('user/update/profile/<int:id>',User_profile_update.as_view()),
    
    
    
    
    path('admin_signin',AdminSignIN.as_view()),
    path('admin_login',AdminLogIn.as_view()),
    path('admin/logout',AdminLogOut.as_view()),
    path('user/details',UserDetails.as_view()),
    path('user/details/<int:id>',UserDetails.as_view()),
    
    
    #Media and Image
    
    path('media/upload',Imageupload.as_view()),
    

    
    
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)















