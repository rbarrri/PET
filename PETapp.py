from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

pdStatement = pd.read_csv('C:/Users/ryang/OneDrive/Documents/PET/2025-09-04_transaction_download.csv')

class Statement():
    content =  pd.read_csv('C:/Users/ryang/OneDrive/Documents/PET/2025-09-04_transaction_download.csv')
    rows = content.index
    columns = content.columns

@app.route('/') #, methods=['POST', 'GET']
def index():
    pdStatement = Statement()
    return render_template('index.html', inStatement = pdStatement)

if __name__ == "__main__":
    app.run(debug=True)