from django.test import TestCase

# Create your tests here.
image_path = "App/media/profile_images/IMG20220212113003.jpg"

full_url =  image_path.lstrip("/")
print(full_url)