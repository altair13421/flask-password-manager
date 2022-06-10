# Flask Simple Password Manager

Simple Password Manager made in Flask

Complete with Login Verification (secure)
sign up, and then sign in
However Password Viewing isn't Secure, as it is Just there in plain text, might fix it later, might not

```export FLASK_APP=main.py```
```export FLASK_ENV=development```
```flask db init```
```flask db migrate -m "users table"```
```flask db upgrade```
```flask db migrate -m "passwords table"```
```flask db upgrade```
```flask run```

goto http://127.0.0.1:5000/