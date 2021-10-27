# Small script that sets development env vars for you and then runs backend
export FLASK_APP=backend
export FLASK_ENV=development
flask run -h localhost -p 5000
