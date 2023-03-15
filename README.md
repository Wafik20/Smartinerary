# Smartinerary
 A travel tool that enables tourists to plan out their daily activities based on the given location and the duration of the stay.

# How to Run 
1. Make a new virtual environment using `python -m venv virtual_env`
2. Once the virtual environment is made, run the command `virtual_env/Scripts/activate`
3. Run the command `pip install -r requirements.txt` in the virtual environment
4. Run the command `$env:FLASK_APP = "smartinerary.py"` in the virtual environment
5. `flask initdb` initializes the database 
6. `flask run` runs the app