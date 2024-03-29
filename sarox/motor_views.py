# from django.db import IntegrityError
# from django.db import models
# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from .models1 import CustomUser,AdminTables,UserTokenTable,AdminStatusTable,AdminTokenTable,OTPVerification_TABLE,profile_image_table,StatusToken
# from rest_framework.decorators import api_view
# from .serializers1 import UserSerializer,AdminSerializer,UserTokenSerializer,AdminStatusChangeSerializer,AdminTokenSerializer,ImageSerializer
# from rest_framework.permissions import IsAuthenticated
# import jwt,datetime
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models1 import Motor_tables
# from .serializers1 import MotorSerializer
# from django.contrib.auth import authenticate
# from rest_framework.views import APIView
# from rest_framework.exceptions import AuthenticationFailed

# class MotorRegistrations(APIView):
#     def post(self, request):
#         token = request.headers.get('Authorization')

#         if not token:
#             raise AuthenticationFailed('Token is required for this operation')

#         # The token obtained from the header might be prefixed with "Bearer "
#         # Remove the "Bearer " prefix if present
#         token = token.replace('Bearer ', '')
        

#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Token has expired')
#         except jwt.InvalidTokenError:
#             raise AuthenticationFailed('Invalid token')

#         user_id = payload['id']

#         # Retrieve the token instance from the AdminTokenTable
#         try:
#             token_instance = AdminTokenTable.objects.get(user_id=user_id, token_store=token)
#             serializer = MotorSerializer(data=request.data)

#             if serializer.is_valid():
#                 motors = serializer.save()


#                 return Response({
#                     "message": "Motor Register Successfull",

#                     "data": serializer.data,
#                 # "token": str(refresh.access_token),
#                 }, status=status.HTTP_200_OK)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except AdminTokenTable.DoesNotExist:
#             return Response({'error': 'Invalid token', 'status': status.HTTP_404_NOT_FOUND},status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error':'internal server error','status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        
# #with token display list of motor list
# @api_view(['GET'])
# def get_mot_info_by_token(request, motor_id=None):
#         token = request.headers.get('Authorization')

#         if not token:
#             raise AuthenticationFailed('Token is required for this operation')

#         # The token obtained from the header might be prefixed with "Bearer "
#         # Remove the "Bearer " prefix if present
#         token = token.replace('Bearer ', '')
        

#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Token has expired')
#         except jwt.InvalidTokenError:
#             raise AuthenticationFailed('Invalid token')

#         user_id = payload['id']

#         # Retrieve the token instance from the AdminTokenTable
#         try:
#             token_instance = AdminTokenTable.objects.get(user_id=user_id, token_store=token)
#             if not token_instance:
#                 return Response({'error': 'Invalid token', 'status': status.HTTP_404_NOT_FOUND},status.HTTP_400_BAD_REQUEST)
                
 
#             if motor_id is None:
#                 motors = Motor_tables.objects.all()
#                 serializer = MotorSerializer(motors, many=True)

#                 return Response({'message': 'motors get successful', 'data': serializer.data,'status':status.HTTP_200_OK},status.HTTP_200_OK)
            
#             if motor_id:
#                 motors=Motor_tables.objects.get(motor_id=motor_id)
#                 serializer=MotorSerializer(motors)
#                 return Response({'message': 'motor get successful', 'data': serializer.data,'status':status.HTTP_200_OK},status.HTTP_200_OK)
#         except AdminTokenTable.DoesNotExist:
#             return Response({'error': 'Invalid token', 'status': status.HTTP_404_NOT_FOUND},status.HTTP_400_BAD_REQUEST)
#         except Motor_tables.DoesNotExist:
#             return Response({'error': 'Motor not found','status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error':'internal server error','status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        
        
# #without token display list of motor list 


# class Display_motor(APIView):
#     def get(self,request,motor_id=None):
#         try:
#             if motor_id is None:
#                 motors=Motor_tables.objects.all()
            
#                 serializer=MotorSerializer(motors,many=True)
#                 return Response({'message': 'motors get successful', 'data': serializer.data,'status':status.HTTP_200_OK},status.HTTP_200_OK)
#             if motor_id:
#                 motor=Motor_tables.objects.get(motor_id=motor_id)
#                 serializer=MotorSerializer(motor)
#                 return Response({'message': 'motors get successful', 'data': serializer.data,'status':status.HTTP_200_OK},status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error':'internal server error','status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    
    
    
    
# # get motor information using motor_id


# @api_view(['GET'])
# def get_mot_by_motorID(request, motor_id=None):
#     try:
#         if motor_id is None:
#             motors = Motor_tables.objects.all()
#             serializer = MotorSerializer(motors, many=True)
#         else:
#             motors = Motor_tables.objects.get(motor_id=motor_id)
#             serializer = MotorSerializer(motors)
#         return Response({'message': 'Get operation successful', 'data': {
#             'motor_name':motors.motor_name,
#             'power_circuit':motors.power_circuit,
#             'power_quality':motors.power_quality,
#             'insulation':motors.insulation,
#             'rotor':motors.rotor,
#             'stator':motors.stator,
#             'airgap':motors.airgap,
     
            
#             },'status':status.HTTP_200_OK})
#     except Motor_tables.DoesNotExist:
#         return Response({'error': 'Motor not found','status':status.HTTP_404_NOT_FOUND})
# @api_view(['GET'])
# def get_mot_by_killowatt(request, killowatt=None):
#     try:
#         if killowatt is None:
#             motors = Motor_tables.objects.all()
#             serializer = MotorSerializer(motors, many=True)
#         else:
#             motors = Motor_tables.objects.filter(killowatt=killowatt)
#             serializer = MotorSerializer(motors, many=True)

#         motor_data = [
#             {
#                 'motor_name': motor['motor_name'],
#                 'power_circuit': motor['power_circuit'],
#                 'power_quality': motor['power_quality'],
#                 'insulation': motor['insulation'],
#                 'rotor': motor['rotor'],
#                 'stator': motor['stator'],
#                 'airgap': motor['airgap'],
#             }
#             for motor in serializer.data
#         ]

#         return Response({'message': 'Get operation successful', 'data': motor_data, 'status': status.HTTP_200_OK})

#     except Motor_tables.DoesNotExist:
#         return Response({'error': 'Motor not found', 'status': status.HTTP_404_NOT_FOUND})
# @api_view(['GET'])
# def get_mot_by_voltage(request, voltage=None):
#     try:
#         if voltage is None:
#             motors = Motor_tables.objects.all()
#             serializer = MotorSerializer(motors, many=True)
#         else:
#             motors = Motor_tables.objects.filter(voltage=voltage)
#             serializer = MotorSerializer(motors, many=True)

#         motor_data = [
#             {
#                 'motor_name': motor['motor_name'],
#                 'power_circuit': motor['power_circuit'],
#                 'power_quality': motor['power_quality'],
#                 'insulation': motor['insulation'],
#                 'rotor': motor['rotor'],
#                 'stator': motor['stator'],
#                 'airgap': motor['airgap'],
#             }
#             for motor in serializer.data
#         ]

#         return Response({'message': 'Get operation successful', 'data': motor_data, 'status': status.HTTP_200_OK})

#     except Motor_tables.DoesNotExist:
#         return Response({'error': 'Motor not found', 'status': status.HTTP_404_NOT_FOUND})
# @api_view(['GET'])
# def get_mot_by_locations(request, locations=None):
#     try:
#         if locations is None:
#             motors = Motor_tables.objects.all()
#             serializer = MotorSerializer(motors, many=True)
#         else:
#             motors = Motor_tables.objects.filter(locations=locations)
#             serializer = MotorSerializer(motors, many=True)

#         motor_data = [
#             {
#                 'motor_name': motor['motor_name'],
#                 'power_circuit': motor['power_circuit'],
#                 'power_quality': motor['power_quality'],
#                 'insulation': motor['insulation'],
#                 'rotor': motor['rotor'],
#                 'stator': motor['stator'],
#                 'airgap': motor['airgap'],
#             }
#             for motor in serializer.data
#         ]

#         return Response({'message': 'Get operation successful', 'data': motor_data, 'status': status.HTTP_200_OK})

#     except Motor_tables.DoesNotExist:
#         return Response({'error': 'Motor not found', 'status': status.HTTP_404_NOT_FOUND})
    
    
# class motor_update(APIView):
#     def put(self,request,motor_id=None):
#         token = request.headers.get('Authorization')

#         if not token:
#             raise AuthenticationFailed('Token is required for this operation')

#         # The token obtained from the header might be prefixed with "Bearer "
#         # Remove the "Bearer " prefix if present
#         token = token.replace('Bearer ', '')
        

#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Token has expired')
#         except jwt.InvalidTokenError:
#             raise AuthenticationFailed('Invalid token')

#         user_id = payload['id']

#         # Retrieve the token instance from the AdminTokenTable
#         try:
#             token_instance = AdminTokenTable.objects.get(user_id=user_id, token_store=token)
#             if not token_instance:
#                 return Response({'error': 'Invalid token', 'status': status.HTTP_404_NOT_FOUND},status.HTTP_400_BAD_REQUEST)
#             if motor_id is None:
#                 return Response({'error':'Motor id has required to update','status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
#             if motor_id:
#                 motor=Motor_tables.objects.filter(motor_id=motor_id).first()
                
#                 if motor:
#                     serializer = MotorSerializer(motor, data=request.data, partial=True)
#                     if serializer.is_valid():
#                         serializer.save()
#                         return Response({'message': 'Motor updated successfully', 'data': serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
#                     else:
#                         return Response({'error': 'Motor not update','status':status.HTTP_304_NOT_MODIFIED}, status=status.HTTP_304_NOT_MODIFIED)
#                 else:
#                     return Response({'error': 'Motor not found','status':status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
                        
                        
                    
            
#         except AdminTokenTable.DoesNotExist:
#             return Response({'error': 'Invalid token', 'status': status.HTTP_404_NOT_FOUND},status.HTTP_400_BAD_REQUEST)
#         except Motor_tables.DoesNotExist:
#             return Response({'error': 'Motor not found','status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error':'internal server error','status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            
        



# @api_view(['PUT'])
# def update_mot_info(request, motor_id=None):

        
#     try:
       
                
#         if motor_id:
            

#             motor = Motor_tables.objects.get(motor_id=motor_id)
            
#             if motor:
                
#                 serializer = MotorSerializer(motor, data=request.data, partial=True)
#                 if serializer.is_valid():
#                     serializer.save()
#                     return Response({'message': 'Motor updated successfully', 'data': serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({'error': serializer.errors,'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({'error': 'Motor not found','status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
#         else:
#             return Response({'error': 'motor_id is required for update','status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
                

#     except Motor_tables.DoesNotExist:
#         return Response({'error': 'Motor not found','status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({'error':'internal server error','status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['DELETE'])
# def delete_mot_info(request, motor_id=None):
#     try:
#         if motor_id is None:
#             return Response({'error': 'Equip type is required for delete'}, status=status.HTTP_400_BAD_REQUEST)

#         motor = Motor_tables.objects.get(motor_id=motor_id)
#         deleted_data = MotorSerializer(motor).data  # Serialize the deleted data before deleting
#         motor.delete()
#         return Response({'message': 'Motor deleted successfully', 'deleted_data': deleted_data}, status=status.HTTP_200_OK)
#     except Motor_tables.DoesNotExist:
#         return Response({'error': 'Motor not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    
    
# #make an api based on user id to assign motor id

# class AssignMotor(APIView):
#     def post(self,request,motors_id=None):
#         user_id=request.data.get('user_id')
#         motors_id=request.data.get('motors_id')
#         print("types",type(motors_id))
#         print(len(motors_id))
#         # gdjhsgsah
        
#         if not user_id:
#             return Response({'message':'user id is wrong','status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
#         if not motors_id :
#             return Response({'message':'motor id is wrong','status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
        
#         user=CustomUser.objects.filter(id=user_id).first()
#         user.No_of_motor=len(motors_id)
#         user.motor_id=motors_id
#         # user.motor_name=motors_name_list
#         user.save()
#         if not user:
#             return Response({'message':'user not defined','status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
      
            
        
#         try:
#             motor_list = []  # List to store the retrieved motors
            

#             for mot_id in motors_id:
#                 motor = Motor_tables.objects.filter(motor_id=mot_id).first()
#                 # print('ms',motor)

#                 if motor:
#                     motors = Motor_tables.objects.get(motor_id=mot_id)
               
                    
#                     serializer = MotorSerializer(motors)
                    

                    

#                 else:
#                      return Response({'message': 'Invalid motor id', 'status': status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)


#             return Response({'message': 'Assigned motors to user', 'data': motor_list, 'status': status.HTTP_200_OK})


            
#         except CustomUser.DoesNotExist:
#             return Response({'message':'internal servere error','status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
#         except Motor_tables.DoesNotExist:
#             return Response({'message':'internal servere error','status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
        
            
        
# #Assign motors using user id -------------------------------------------------------------------
# class AssignMotorByID(APIView):
#     def post(self,request,user_id=None):
#         # user_id=request.data.get('user_id')
#         motors_id=request.data.get('motors_id')

        
#         user=CustomUser.objects.filter(id=user_id).first()
#         if not user_id:
#             return Response({'message':'user id is wrong','status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
#         # if not motors_id :
#         #     user.No_of_motor=len(motors_id)
#         #     user.motor_id=motors_id
            
            
#         #     user.is_approved=False
#         #     user.save()
#         #     return Response({'message':'assigned motor updated successfully','status':status.HTTP_200_OK},status.HTTP_200_OK)
        

        
        

#         if not user:
#             return Response({'message':'user not defined','status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
      
            
        
#         try:
#             if not motors_id :
#             #    user.No_of_motor=len(motors_id)
#             #    user.motor_id=motors_id
#             #    user.is_approved=False
#             #    user.motor_names=0
#             #    user.save()
#                 token = UserTokenTable.objects.filter(user_id=user.id).first()
#                 if token is None:
#                     user.No_of_motor=len(motors_id)
#                     user.motor_id=motors_id
#                     user.is_approved=False
                   
#                     user.motor_names=0
                    
#                     user.save()
#                     serializer=UserSerializer(user)
#                     return Response({'message':'assigned motor updated successfully','data':serializer.data,'status':status.HTTP_200_OK},status.HTTP_200_OK)

#                 if token:
#                     user.No_of_motor=len(motors_id)
#                     user.motor_id=motors_id
                          
#                     token.delete()
#                     user.is_approved=False
                   
#                     user.motor_names=0
                   
#                     user.save()
#                     serializer=UserSerializer(user)
#                     return Response({'message':'assigned motor updated successfully','data':serializer.data,'status':status.HTTP_200_OK},status.HTTP_200_OK)
                    
#                 return Response({'message':'assigned motor updated successfully','status':status.HTTP_200_OK},status.HTTP_200_OK)
#             if motors_id:
#                 user.No_of_motor=len(motors_id)
#                 user.motor_id=motors_id
#                 user.save()
                
#                 motor_list = []  # List to store the retrieved motors
#                 motors_name_list=[] #list to store the retrieve motors name
            
#                 for mot_id in motors_id:
#                     motor = Motor_tables.objects.filter(motor_id=mot_id).first()
                

#                     if motor:

#                         user.is_approved=True
#                         user.save()
                    
#                         motors = Motor_tables.objects.get(motor_id=mot_id)
                        
#                         serializer = MotorSerializer(motors)
#                         motor_list.append(serializer.data)
                        
                        
#                         motor_names=motor.motor_name
#                         motors_name_list.append(motor_names)
#                     if not motor:
                    
#                         return Response({'message': 'please assign atleast one motor', 'status': status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)
                        
           
#                 user.motor_names=motors_name_list
  
#                 user.save()

#                 return Response({'message': 'Assigned motors to user', 'data': motor_list, 'status': status.HTTP_200_OK})
      


            
#         except CustomUser.DoesNotExist:
#             return Response({'message':'internal servere error','status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
#         except Motor_tables.DoesNotExist:
#             return Response({'message':'internal servere error','status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
        
            
# class Checkstatus(APIView):
#     def get(self, request,user_id=None):
  
#         try:
#             if not user_id:
#                 return Response({"Message": "Invalid user",'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
   
#             user = CustomUser.objects.filter(id=user_id).first()

            
#             if user.is_approved:
#                 serializer=UserSerializer(user)
                
#                 # generate a token
#                 payload = {
#                     'id': user.id,
#                     'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
#                     'iat': datetime.datetime.utcnow(),
#                     }
#                 secret_key = 'secret'
#                 token = jwt.encode(payload=payload, key=secret_key, algorithm='HS256')
#         # token=jwt.PyJWT.encode(payload=payload, key=secret_key, algorithm='HS256')

#         # Check if an existing token entry exists for the user
#                 token_table_instance = StatusToken.objects.filter(id=user.id).first()

#         # If an existing token entry exists, update the token, else create a new entry
#                 if token_table_instance:
#                     token_table_instance.token_store = token
#                     token_table_instance.save()
#                 else:
#                     token_table_instance = StatusToken.objects.create(
#                     id=user.id,
#                     token_store=token,
#                     email=user.email
#                 )

#                 response = Response(status=status.HTTP_200_OK)
#                 response.data = {
                    
#                     'message': 'User approved succsessful',
#                     'token': token,
#                     'data':serializer.data,
#                     'token_table_id': token_table_instance.id,
#                     'status': status.HTTP_200_OK,
#                 }

#                 return response
#             if not user.is_approved:
#                 return Response({"Message": "user disapproved ",'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
#         except Exception as e:
#             return Response({"message":'internal server error','status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
        
