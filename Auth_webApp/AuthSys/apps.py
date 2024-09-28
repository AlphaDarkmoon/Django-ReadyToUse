from django.apps import AppConfig  # Import Django's AppConfig for application configuration

class AuthsysConfig(AppConfig):
    """
    Configuration class for the AuthSys application.

    This class is used to configure the application and set its name 
    and default field types.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Specify the default auto field type for models
    name = 'AuthSys'  # Set the name of the application
