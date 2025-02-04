from app import create_app
from app.models import Patient, Test, TestRepetition, TestSetup, User

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)