from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) #i'll remove debug=true for pythonanywhere