## MAIN FILE THAT CREATES THE FLASK APP
## SMARTINERARY TRAVEL APP
##
##
##
from website import create_app

app = create_app()

# run the app
if __name__ == '__main__':
    app.run(debug=True)
