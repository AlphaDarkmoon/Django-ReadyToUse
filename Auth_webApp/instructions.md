## Instructions for Setting Up the Project

1. Create a .env File

* Copy the contents of .env.example to create a new file named .env in the main directory of your project.


2. Update the ```INSTALLED_APPS``` Setting

* Open your settings file and locate the INSTALLED_APPS list.
* Replace "Home" with the name of your Home app. Ensure the list includes the Auth handling app as shown below:

```
INSTALLED_APPS = [
    ...
    "YourHomeAppName",  # Replace with your Home app name
    "SysAuth",          # This is the Auth handling app
]
```
3. Modify URL Patterns in urls.py (Home App)

* Navigate to the urls.py file in your Home app directory.
* Update the URL patterns to reflect the routes for your applications.

4. Organize HTML Templates

* Ensure that all HTML templates for the AuthSys app are located in the following directory:
```
AuthSys > templates > AuthSys
```
5. Update App Name in URL References

* In your HTML files, ensure that you reference the correct app name in the URL template tags. For example:
```
{% url 'YourAppName:login' %}
```
