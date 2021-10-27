# Python_web
Python web server where you can successfully login and send token.
## Instalation
Program uses flask, flask_sqlalchemy and pyjwt.

```shell
-pip install Flask
-pip install Flask-SQLAlchemy
-pip install PyJWT
OR
pip install -r requirements.txt
```

## Usage

To run type these commands:

```shell
cd src/
python3 pyth_web.py
```

## Examples

Here is the example of usage:

```shell
After runng go straight to localhost:5000/login 
Choose one of this Accounts 
Login: admin
Password: password
Login: john 
Password: doe
Login: alice
Password: bob
After Getting Your token type this: localhost:5000/protected?token={your token}
