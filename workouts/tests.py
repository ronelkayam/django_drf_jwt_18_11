from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Workout
from .mongo_client import get_audit_collection

# Create your tests here.


class DualDBWorkoutAPITests(APITestCase):
    """
    1.הרשמה והתחברות עם JWT
    2. חסימה לגישה ללא טוקן
    3. ולדציה של DRF (משקל שלילי)
    4. הפעלה של signals
    """
    def setUp(self):
        self.register_url = reverse('auth_register')
        self.login_url = reverse('token_obtain_pair')
        self.workouts_url = reverse('workout_list_create')
        self.logs_url = reverse('mongo_audit_log')


        self.test_username = "test_99"
        self.test_password = "StrongPass1!"
        self.user = User.objects.create_user(
            username=self.test_username,
            password=self.test_password
        )

        self.mongo_collection = get_audit_collection()
        self.mongo_collection.delete_many({"username":self.test_username})

    def tearDown(self):
        self.mongo_collection.delete_many({"username":self.test_username})

    def _authenticate_client(self):
        response = self.client.post(self.login_url,{
            'username': self.test_username,
            'password': self.test_password
        },format='json')

    def test_unauthenticated_access_is_blocked(self):
        response = self.client.get(self.workouts_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_register_and_login_jet_flow(self):
        reg_response = self.client.post(self.register_url,{
            'username':"new_student",
            'email':'student@college.com',
            'password1':'Pass1234',
        },format='json')
        self.assertEqual(reg_response.status_code, status.HTTP_201_CREATED)

        login_response = self.client.post(self.login_url,{
            "username":"new_student",
            "password":"Pass123",

        },format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access',login_response.data)
        self.assertIn('refresh',login_response.data)


    def test_serializer_validation_blocks_navigate_weight(self):
        self._authenticate_client()
        response = self.client.post(self.workouts_url,{
            'exercise_name':'Deadlift',
            'weight_kg':-50,
            'repr':5
        },format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('weight_kg',response.data)


    def test_create_workout_triggers_signal_to_mongodb(self):
        self._authenticate_client()

        payload={
            'exercise_name':'Squat',
            'weight_kg':120.5,
            'repr':12
        }
        response = self.client.post(self.workouts_url,payload,format='json')


        #validate request save in sql server
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.filter(user=self.user).count(), 1)

        #validate signal working - added to Mongo
        mongo_log = self.mongo_collection.find_one({"username":self.test_username})
        self.assertIsNotNone(mongo_log,"don't added to mongo!")
        self.assertEqual(mongo_log["event"],"WORKOUT CREATED")
        self.assertEqual(mongo_log["details"]["exercise"], "Squat")
        self.assertEqual(mongo_log["details"]["weight_kg"],120.5)

        #validate end point /api/logs get from mongo
        logs_response = self.client.get(self.logs_url)
        self.assertEqual(logs_response.status_code, status.HTTP_200_OK)
        self.assertEqual(logs_response.data["total_events"],1)