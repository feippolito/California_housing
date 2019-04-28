import pandas as pd
from flask import Flask, redirect, url_for, request
import sys
from housing import Housing 

app = Flask(__name__)

@app.route('/housing',methods = ['POST', 'GET'])
def housing():
    if request.method == 'POST':
        var_1 = request.form['nm1']
        var_2 = request.form['nm2']
        var_3 = request.form['nm3']
        var_4 = request.form['nm4']
        var_5 = request.form['nm5']
        var_6 = request.form['nm6']
        var_7 = request.form['nm7']
        var_8 = request.form['nm8']
        var_9 = request.form['nm9']
        var_10 = request.form['nm10']

        n_kneighbors = int(request.form['n'])

        fvar_1 = float(var_1)
        fvar_2 = float(var_2)
        fvar_3 = float(var_3)
        fvar_4 = float(var_4)
        fvar_5 = float(var_5)
        fvar_6 = float(var_6)
        fvar_7 = float(var_7)
        fvar_8 = float(var_8)
        fvar_9 = float(var_9)
        
        house1 = Housing()
        list_var = [fvar_1, fvar_2, fvar_3, fvar_4, fvar_5, fvar_6, fvar_7, fvar_8, fvar_9, var_10]

        df = house1.findKneighbors(list_var, n_kneighbors)
        
        return df.to_html(header="true", table_id="table")
    else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = var_1))

if __name__ == '__main__':
   app.run(debug = True)