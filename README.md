# BeWyse_Assignment

The assignment was focused on developing backend system for the endpoints **/accounts/login/, /accounts/register/, /accounts/profile/view, /accounts/profile/edit.**

I have implemented firebase authentication and used local MongoDB Database for storing the information.

## Registration

Registration part takes **email and password** as required fields and rest are optional (i.e first name, last name, username).
After successful registration we receive a **status=200** with the JsonResponse containing username(if provided) and email.

## Login
Login takes **email and password** as credentials to login using **firebase authentication**.
It returns a **status=200** with JsonResponse containing the email, username, full name along with the custom token.
In case of invalid email or password we get an error of **401 Unauthorized**.

## Profile View
It takes only username as parameter in GET request along with the custom token provided while logging.
In case of invalid custom token it throws an **error 401 Unauthorized**.
The username has to be passed in the **URL as a param** to get the profile details. _for eg: 127.0.0.1:8000/accounts/profile/view/?username=username_.
It returns with a JsonResponse containing username, email and full name.
For full name a serializer has been used that combines the first name and last name and returns the full name.

## Profile Edit
The profile edit allows to modify username, firstname and last name _(Any of these or all of them)_.
After passing the body containing any of these, the changes are updated in the local MongoDB Database and it returns the JsonResponse containing the fields that were updated.
First and last name can be similar to already present data in database, but there is a check for usernames so that only unique usernames get stored.
In case of providing already existing username it throws an error containing the response _error : a user with that username already exists._

## Middleware
I have added a custom middleware named **FirebaseAuthenticationMiddleware** which is added to Middlewares list in settings.py for user authentication.

