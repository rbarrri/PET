from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # to create db. flask --app PETapp.py shell , then db.create_all()
db = SQLAlchemy(app)

#pdStatement = pd.read_csv('C:/Users/ryang/OneDrive/Documents/PET/2025-09-04_transaction_download.csv')

class Statement():
    content =  pd.read_csv('C:/Users/ryang/OneDrive/Documents/PET/2025-09-04_transaction_download.csv')
    rows = content.index
    columns = content.columns

class dbStatement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paid = db.Column(db.Integer, nullable=False, default=0)
    trans_date = db.Column(db.String(200), nullable=False)
    posted_date = db.Column(db.String(200), nullable=False)
    card_num = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), nullable=False)
    debit = db.Column(db.Float)
    credit = db.Column(db.Float)

    def __repr__(self):
        return 'Trans %r' % self.id

@app.route('/') #, methods=['POST', 'GET']
def index():
    # Get the csv data a way that wont readd all transactions to the database each time the web page is refreshed
    # get data from csv
    dfTrans =  pd.read_csv('C:/Users/ryang/OneDrive/Documents/PET/2025-09-04_transaction_download.csv')
    
    len = dfTrans.index # amount of rows
    for i in len:
        # create the db object
        new_trans = dbStatement()
        # assign the cvs values
        print(new_trans)
        new_trans.paid = False
        print(new_trans.paid)
        new_trans.trans_date = dfTrans.loc[i, "Transaction Date"]
        print(new_trans.trans_date)
        new_trans.posted_date = dfTrans.loc[i, "Posted Date"]
        print(new_trans.posted_date)
        new_trans.card_num = dfTrans.loc[i, "Card No."].item()
        print(new_trans.card_num)
        new_trans.description = dfTrans.loc[i, "Description"]
        print(new_trans.description)

        if np.isnan(pd.to_numeric(dfTrans.loc[i, "Category"], errors='coerce')):
            new_trans.category = ""
        else:
            new_trans.category = dfTrans.loc[i, "Category"]
        print(new_trans.category)

        if np.isnan(dfTrans.loc[i, "Debit"]):
            new_trans.debit = 0
        else:
            new_trans.debit = dfTrans.loc[i, "Debit"]
        print(new_trans.debit)

        if np.isnan(dfTrans.loc[i, "Credit"]):
            new_trans.credit = 0
        else:
            new_trans.credit = dfTrans.loc[i, "Credit"]
        print(new_trans.credit)

        #try:
        print("Before commit")
        db.session.add(new_trans)
        db.session.commit()
            

        #except:
        #    return 'There was an error adding a transaction'

        # add each row column to the database

    qStatement = dbStatement.query.order_by(dbStatement.posted_date).all()
    return render_template('index.html', inStatement = qStatement)
    #for loop to populate database for each data frame row
    #pass the result of the query to data base to the html

    #pdStatement = Statement()
    #return render_template('index.html', inStatement = pdStatement)
@app.route('/add')
def add(id):
    # To do: update to add statement here
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting task: ' + id
    
if __name__ == "__main__":
    app.run(debug=True)