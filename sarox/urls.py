from django.urls import path
from .views import UserSignIN,UserLogIn,AdminSignIN,AdminLogIn,AdminLogOut,UserLogOut,Imageupload,UserDetails,User_profile_update,WeekProgram,ByCourseName,CourseTable1Reg
# from django.conf import settings
# from django.conf.urls.static import static
from .views import GetAllCourse,UpdateInCT1,GetAllCourseByUser,ByCourseID,forgetPassword,CourseName,DeleteCoach
from .surveyViews import CreateSurvey,getAllSurvey,updateSurvey,deleteSurvey


urlpatterns = [

    path('createCoach',UserSignIN.as_view()),
    path('user/login',UserLogIn.as_view()),
    path('user/logout',UserLogOut.as_view()),
    path('user/update/profile/<int:id>',User_profile_update.as_view()),
    path('forgetPassword',forgetPassword.as_view()),
    
    
    
    
    path('admin_signin',AdminSignIN.as_view()),
    path('admin_login',AdminLogIn.as_view()),
    path('admin/logout',AdminLogOut.as_view()),
    path('getAllCoach',UserDetails.as_view()),
    path('getCoachbyId<int:id>',UserDetails.as_view()),
    
    path('deletCoachbyID/<int:id>',DeleteCoach.as_view()),
    
    
    #Media and Image
    
    path('media/upload',Imageupload.as_view()),
    path('createCourse',WeekProgram.as_view()),
    # path('getAllCourse',ByCourseName.as_view()),
    path('getCoursebyId/<int:cid>',ByCourseName.as_view()),
    path('getAllCourse',CourseName.as_view()),
    path('post/course',CourseTable1Reg.as_view()),
    path('get/course',GetAllCourse.as_view()),
    path('get/course/<int:id>',GetAllCourse.as_view()),
    path('update/course/<int:id>',UpdateInCT1.as_view()),
    path('get/all/course/user',GetAllCourseByUser.as_view()),
    path('get/details/course/by/<int:id>',ByCourseID.as_view()),
    
    
    
    # Suvey table urls
    
    path('createSurvey',CreateSurvey.as_view()),
    path('getAllSurvey',getAllSurvey.as_view()),
    path('updateSurveyById/<int:id>',updateSurvey.as_view()),
    path('deleteSurveyById/<int:id>',deleteSurvey.as_view()),

    
    
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)















