from django.apps import AppConfig


class WorkoutsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workouts'

    def ready(self):
        #שהאפליקציה עולה לאוויר הוא מייבא את קובץ הsignals.py
        import workouts.signals