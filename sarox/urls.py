from django.urls import path
from .views import UserSignIN,UserLogIn,AdminSignIN,AdminLogIn,AdminLogOut,UserLogOut,Imageupload,UserDetails,User_profile_update,WeekProgram,ByCourseName,CourseTable1Reg
# from django.conf import settings
# from django.conf.urls.static import static
from .views import GetAllCourse,UpdateInCT1,GetAllCourseByUser,ByCourseID,forgetPassword,CourseName,DeleteCoach,deleteCourse
from .surveyViews import CreateSurvey,getAllSurvey,updateSurvey,deleteSurvey,getAllTypeSurvey
from .mail import sendMail,videoUpload,postThought,getAllVideo,getAllThoughts,deleteThoughts,deleteVideo,updateVideo
from .program import CreateallProgram,getAllProgram,deleteProgram,updateProgram,AssignCourseByemail,GetAssignCourseofCoach,activeCourse,archiveCourse
from .archive import archiveCourses,CoachDashboard

# from .google_api import GenerateForm
# from .api import CreateGoogleForm
from .views import ResetPassword
from .views2 import GetAllQuestion,deleteQuestions,SubmitQuestions,GetAllPreQuestion,deletePreQuestions,PreSubmitQuestions,PostSubmitQuestions,GetAllPostQuestion,deletePostQuestions
from .generate_pdf import Mid_generate_pdf,Post_generate_pdf,Pre_generate_pdf





urlpatterns = [

    path('createCoach',UserSignIN.as_view()),
    path('user/login',UserLogIn.as_view()),
    path('user/logout',UserLogOut.as_view()),
    path('user/update/profile/<int:id>',User_profile_update.as_view()),
    path('user/update/profile/',User_profile_update.as_view()),
    path('forgetPassword',forgetPassword.as_view()),
    path('setNewPassword',ResetPassword.as_view()),
    
    
    
    
    path('admin_signin',AdminSignIN.as_view()),
    path('admin_login',AdminLogIn.as_view()),
    path('admin/logout',AdminLogOut.as_view()),
    path('getAllCoach',UserDetails.as_view()),
    path('getCoachbyId/<int:id>',UserDetails.as_view()),
    
    
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
    path('getAllSurvey/<str:Surv_type>',getAllTypeSurvey.as_view()),
    path('updateSurveyById/<int:id>',updateSurvey.as_view()),
    path('deleteSurveyById/<int:id>',deleteSurvey.as_view()),
    
    
    #course
    path('deleteCourseByCourseId/<int:cid>',deleteCourse.as_view()),
    path('deleteCourseByCourseId/',deleteCourse.as_view()),
    
    
    path('sendMail',sendMail.as_view()),
    path('uploadVideo',videoUpload.as_view()),
    path('postThoughts',postThought.as_view()),
    path('getAllVideo/<int:id>',getAllVideo.as_view()),
    path('getAllVideo/',getAllVideo.as_view()),
    path('getAllThoughts/<int:id>',getAllThoughts.as_view()),
    path('getAllThoughts/',getAllThoughts.as_view()),
    path('deleteThoughts/<int:id>',deleteThoughts.as_view()),
    path('deleteThoughts/',deleteThoughts.as_view()),
    path('deleteVideos/<int:id>',deleteVideo.as_view()),
    path('deleteVideos/',deleteVideo.as_view()),
    path('updateVideos/<int:id>',updateVideo.as_view()),
    path('updateVideos/',updateVideo.as_view()),
    
    
    
    path('CreateallProgram',CreateallProgram.as_view()),
    path('getAllProgram/<int:pid>',getAllProgram.as_view()),
    path('getAllProgram/',getAllProgram.as_view()),
    path('deleteProgram/<int:pid>',deleteProgram.as_view()),
    path('deleteProgram/',deleteProgram.as_view()),
    path('updateProgram/<int:pid>',updateProgram.as_view()),
    path('updateProgram/',updateProgram.as_view()),
    
    
    
    path('AssignCourseByemail/<str:email>',AssignCourseByemail.as_view()),
    path('AssignCourseByemail/',AssignCourseByemail.as_view()),
    path('GetAssignCourseofCoach/<str:email>',GetAssignCourseofCoach.as_view()),
    path('GetAssignCourseofCoach/',GetAssignCourseofCoach.as_view()),
    
    path('activeCourse/<str:email>/<int:cid>/<str:week>',activeCourse.as_view()),
    path('activeCourse/<str:email>//<str:week>',activeCourse.as_view()),
    path('activeCourse//<int:cid>/<str:week>',activeCourse.as_view()),
    path('activeCourse/',activeCourse.as_view()),
    path('activeCourse/<str:email>/<int:cid>/',activeCourse.as_view()),
    path('archiveCourses/<str:email>',archiveCourses.as_view()),
    path('archiveCourses/',archiveCourses.as_view()),
    path('CoachDashboard/<str:email>',CoachDashboard.as_view()),
    path('CoachDashboard/',CoachDashboard.as_view()),
    
    # path('googleform',GenerateForm.as_view()),

    path('midSurveyQuestions',SubmitQuestions),
    path('GetAllMidSurveyQuestion/<str:email>',GetAllQuestion.as_view()),
    path('GetAllMidSurveyQuestion',GetAllQuestion.as_view()),
    path('deleteMidSurveyQuestions',deleteQuestions.as_view()),
    path('preSurveyQuestions',PreSubmitQuestions),
    # path('GetAllQuestion/<str:email>',GetAllQuestion.as_view()),
    path('GetAllPreSurveyQuestion',GetAllPreQuestion.as_view()),
    path('deletePreSurveyQuestions',deletePreQuestions.as_view()),
    path('postSurveyQuestions',PostSubmitQuestions),
    path('GetAllPostSurveyQuestion/<str:email>',GetAllPostQuestion.as_view()),
    path('GetAllPostSurveyQuestion',GetAllPostQuestion.as_view()),
    path('deletePostSurveyQuestions',deletePostQuestions.as_view()),
    path('MidSurveyPdf',Mid_generate_pdf),
    path('PostSurveyPdf',Post_generate_pdf),
    path('PreSurveyPdf',Pre_generate_pdf)
    
    
    
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
















