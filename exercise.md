Lab Exercises: Extending the DRF + JWT + Dual-DB Project

Complete the following three progressive exercises on top of the existing project codebase.

Level 1 (Easy): Add a notes Field Across SQL Server & MongoDB

Open workouts/models.py and add an optional notes field (CharField or TextField with blank=True, null=True) to the Workout model.

Run python manage.py makemigrations and python manage.py migrate to update the SQL Server table.

Add 'notes' to WorkoutSerializer in workouts/serializers.py.

Update the log_workout_saved signal in workouts/signals.py so that notes is also included in the log document sent to MongoDB.

Test: Create a new workout via POST /api/workouts/ with "notes" in the JSON body, then verify it appears in GET /api/logs/.

Level 2 (Medium): Update & Delete Endpoints (WorkoutDetailView)

In workouts/views.py, create WorkoutDetailView inheriting from generics.RetrieveUpdateDestroyAPIView.

Enforce IsAuthenticated and override get_queryset(self) so users can only view, edit, or delete their own workouts (user=self.request.user).

Register the route path('workouts/<int:pk>/', WorkoutDetailView.as_view(), name='workout_detail') in workouts/urls.py.

Test:

Send a DELETE request to /api/workouts/<id>/ and verify that the existing log_workout_deleted signal automatically writes a WORKOUT_DELETED event to MongoDB.

Verify that User A cannot delete User B's workout (should return 404 Not Found).

Level 3 (Hard): Filter MongoDB Audit Logs by Event Type

Update AuditLogView in workouts/views.py to support an optional event query parameter (e.g., GET /api/logs/?event=WORKOUT_CREATED or GET /api/logs/?event=WORKOUT_DELETED).

Read the parameter using request.query_params.get('event').

If provided, include "event": event_type in the MongoDB collection.find() query filter alongside "username": request.user.username.

Test: Call GET /api/logs/?event=WORKOUT_DELETED and verify that only deletion events are returned from MongoDB.