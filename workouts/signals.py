from datetime import datetime, timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Workout
from .mongo_client import get_audit_collection


@receiver(post_save, sender=Workout)
def log_workout_saved(sender, instance, created, **kwargs):
    """
    מופעל אוטומטית מיד אחרי שאימון נשמר
    או עודכן בSQLSERVER
    כותב לוג גמיש לmongo
    """
    collection = get_audit_collection()
    action_type = "WORKOUT_CREATED" if created else "WORKOUT_UPDATED"
    log_document = {
        "event": action_type,
        "sql_workout_id": instance.id,
        "username": instance.user.username,
        "details": {
            "exercise": instance.exercise_name,
            "weight_kg": instance.weight_kg,
            "reps": instance.reps,
            "sets": instance.sets,
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    # הכנסה לMongo בלי תלות בסכמה קשיחה sql server
    collection.insert_one(log_document)
    print(f"[SIGNAL -> MONGO] logged {action_type} for {instance.user.username} ")


@receiver(post_delete, sender=Workout)
def log_workout_deleted(sender, instance, **kwargs):
    collection = get_audit_collection()
    collection.insert_one({
        "event": "WORKOUT_DELETED",
        "sql_workout_id": instance.id,
        "username": instance.user.username,
        "exercise": instance.exercise_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
