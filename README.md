Django REST Framework (DRF) + JWT + Signals (Dual-DB Architecture)A complete, production-style demonstration project illustrating the transition from basic Django (JsonResponse) to an industry-standard RESTful architecture featuring:Django REST Framework (DRF): Automatic data serialization, request parsing, and input validation.JWT Authentication (SimpleJWT): Stateless, token-based user authentication (Bearer tokens).Django Signals (post_save & post_delete): Event-driven architecture decoupling core business logic from side effects.Dual-DB Architecture: Hybrid persistence using SQL Server for relational domain data (Users & Workouts) and MongoDB for flexible, high-speed Audit Logs.Architecture FlowClient (JWT Bearer Token)
   │
   ▼
DRF APIView / GenericView (Authentication & Permissions)
   │
   ▼
DRF Serializer (Validation & Serialization)
   │
   ▼
SQL Server (Saves relational Workout record)
   │
   ├──► [Django Signal: post_save / post_delete] ──► MongoDB (Writes Audit Log document)
PrerequisitesBefore running the project, ensure you have the following installed and running locally:Python 3.11+Microsoft SQL Server with an empty database named GymDRF_DB and ODBC Driver 17 for SQL Server installed.MongoDB Community Server running on mongodb://localhost:27017/.Setup & Installation (Windows CMD)Clone the repository:git clone https://github.com/ronelkayam/django_drf_jwt_18_11.git
cd django_drf_jwt_18_11
Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate.bat
Install dependencies:
pip install -r requirements.txt
Configure environment variables:
Copy the example environment file and adjust the credentials if needed:copy .env.example .env
Run database migrations (SQL Server):
python manage.py makemigrations
python manage.py migrate
Running Automated TestsThe test suite validates JWT protection (401 Unauthorized), serializer validation (400 Bad Request), and live cross-database synchronization between SQL Server and MongoDB via Signals:python manage.py test
Running the Server & API EndpointsStart the development server:python manage.py runserver
Available EndpointsMethodEndpointAuth RequiredDescriptionPOST/api/register/Public (AllowAny)Register a new user in SQL ServerPOST/api/login/Public (AllowAny)Authenticate and receive access & refresh JWT tokensPOST/api/token/refresh/Public (AllowAny)Refresh an expired access tokenGET/api/workouts/JWT BearerRetrieve authenticated user's workouts from SQL ServerPOST/api/workouts/JWT BearerCreate a workout in SQL Server (triggers Signal to MongoDB)GET/api/logs/JWT BearerRetrieve user's event audit history from MongoDBQuick Test via CMD (curl)Register a user:curl -X POST http://127.0.0.1:8000/api/register/ -H "Content-Type: application/json" -d "{\"username\": \"ron_student\", \"password\": \"Password123\"}"
Login to obtain a JWT Access Token:
curl -X POST http://127.0.0.1:8000/api/login/ -H "Content-Type: application/json" -d "{\"username\": \"ron_student\", \"password\": \"Password123\"}"
Create a workout (replace <TOKEN> with your access token):curl -X POST http://127.0.0.1:8000/api/workouts/ -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" -d "{\"exercise_name\": \"Pull Ups\", \"weight_kg\": 15, \"reps\": 12}"
Verify automatic audit logging in MongoDB:
curl -X GET http://127.0.0.1:8000/api/logs/ -H "Authorization: Bearer <TOKEN>"
