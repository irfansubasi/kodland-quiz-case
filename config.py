class Config:
    SECRET_KEY = 'secret_key_here' #given expressly for kodland case review
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quiz.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False