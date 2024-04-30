# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from django.core.mail import send_mail
# from sarox.models1 import Profile

# @receiver(post_save, sender=Profile)
# def send_forget_password_mail(sender, instance, **kwargs):
#     try:
#         print("value of sender",sender)
#         print(f"Type of instance: {type(instance)}")
#         print(f"Value of instance: {instance}")

#         user_email = instance.email  # Assuming 'email' is the field in your Profile model storing the user's email
#         token = instance.forgot_password_token
#         print("user",user_email)
#         print(token)
#         reset_link = f'https://yourwebsite.com/reset-password/{token}/'  # Update with your actual reset password link

#         # Define your email subject and message
#         subject = 'Password Reset Link'
#         message = f"Hello {user_email},\n\nClick the following link to reset your password:\n{reset_link}"

#         # Send the email
#         x = send_mail(
#             subject,
#             message,
#             'email@progrowth.coach',  # Replace with your sender email address
#             recipient_list=[user_email],  # Replace with the recipient email address
#             fail_silently=False,
#         )
#         print(x)

#     except Exception as e:
#         # Handle any exceptions or log errors
#         print(f"Error sending forget password email: {str(e)}")
