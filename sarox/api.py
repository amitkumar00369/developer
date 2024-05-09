from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apiclient import discovery
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials

class CreateGoogleForm(APIView):
    def post(self, request):
        try:
            SCOPES = "https://www.googleapis.com/auth/forms.body"
            DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

            credentials = ServiceAccountCredentials.from_json_keyfile_name("django-422609-46720dc5ed4d.json", SCOPES)

            form_service = discovery.build(
                "forms",
                "v1",
                http=credentials.authorize(Http()),
                discoveryServiceUrl=DISCOVERY_DOC,
                static_discovery=False,
            )

            form = {
                "info": {
                    "title": "My new form",
                },
                "items": [
                    {
                        "title": "Name",
                        "type": "TEXT",
                    },
                    {
                        "title": "Email",
                        "type": "TEXT",
                    },
                    {
                        "title": "Feedback",
                        "type": "TEXT",
                    },
                    {
                        "title": "Mobile Number",
                        "type": "TEXT",
                    },
                ]
            }

            result = form_service.forms().create(body=form).execute()
            print(result)
            
            form_id = result.get('formId')
            form_link = f"https://docs.google.com/forms/d/{form_id}/viewform"

            return Response({'form_link': form_link}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
