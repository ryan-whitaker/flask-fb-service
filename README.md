## Project Overview
### Description
The purpose of this project is to provide a very basic template to handle authentication and general profile management with Flask and Firebase. By using a set of predictable functions and endpoints, you can easily knock out the user management requirement of your Flask/Firebase application by simply integrating this repository with your project or vice-versa.
### Features
- Account management with email, password, and any additional fields you want
- JWT-based authentication with email and password using RS256 encoding
- Predefined routes to call from your client
- Automatic public key extraction from the service account private key
## Getting Started
To get started, you will need Python 3.10 installed, an active Firebase project with email and password authentication enabled and Realtime Database established (Pyrebase will throw an error without the RTDB route).
1. Clone the repository
2. Create a virtual environment in the root of the directory
3. Install the dependencies in requirements.txt
4. Create a .env file in the root of your directory.
5. Add your Firebase service account and config JSON to the .env file you created. Ensure both are single lines, like so:
```
SERVICE_ACCOUNT={"type": "service_account", ...}
CONFIG={"apiKey": "xxxxxx", ...}
```
6. Start the development server by running the dev.py file.
## Usage
- The service runs on port 5000 and each endpoint expects a standard JSON payload.
- The auth.py file in the auth directory handles all the account creation and management. At the time of writing, you can customize the user
- I am assuming functions such as signing up and logging in are unique and therefore the routes are shorter. For profile/account management, I opted for extended URLs under the assumption developers may be deleting or updating more types of information. These routes can be changed in the routes.py file.
### /signup
- Method: POST
- Expected payload is flexible, but at a minimum must contain the new user's email and password
```
{
    "email": "ryan@example.com",
    "password": "xxxxxxx",
}
```
- When a user signs up, it creates a Firebase, retrieves the UID, and creates a document using the UID in a users collection in Firestore to enable the retention of additional user attributes (e.g., Stripe customer ID's, subscription tiers, etc.).
    - Note: Firestore does not capture the user's password for obvious reasons.
- Upon successful account creation, the server will send an object containing a JWT, some non-encoded user data, and an expiresIn value:
```
{
    "token": "xxxxx",
    "expiresIn": 43200,
    "user": {
        "email": "ryan@example.com",
        ...
    }
}
```
### /login
- Method: POST
- Expected payload must contain the user's email and password
```
{
    "email": "ryan@example.com",
    "password": "xxxxxxx"
}
```
- Upon successful authentication, the server queries the users collection in Firestore, retrieves the user data, and returns the same response data as the /signup endpoint.
### /settings/profile/delete
- Method: POST
- Expected payload must contain the user's email and current password as well as the JWT in the Authorization header.
- The server checks the email and username to ensure the user credentials are valid then deletes the Firebase user and associated Firestore data.
### /settings/profile/update
- Method: POST
- This endpoint updates non-credential information and therefore does not require altering the Firebase use.
- Expected payload must contain the user attributes in the Firestore document and the JWT in the Authorization header.
### /settings/email/update
- Method: POST
- Expected payload must include the user's current email and password to verify authenticity and the new email and the JWT in the Authorization header
```
{
    "email": "ryan@example.com",
    "password": "xxxxxxx",
    "new_email": "newryan@example.com"
}
```
### /settings/password/update
- Method: POST
- Expected payload must include the user's current email, password, new password, and confirm password as well as the JWT in the Authorization header
```
{
    "email": "ryan@example.com",
    "password": "xxxxxxx",
    "new_password": "xxxxxxxx",
    "confirm_password": "xxxxxxxx"
}
```
## Additional feature/module integration
To add more of your own modules, create adjacent directories and include an empty __init__.py file. You can use dot notation to import the Flask app into your module to create routes and then similarly import those new routes in the main app.py file.
## To-Do
- Improve error handling and response codes/messages
- Add account recovery (this is a lower priority since Firebase gives you this out of the box but I would still like something a bit more refined)
- Add more standardization and validation to payloads
- Improve naming conventions
