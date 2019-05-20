import pandas as pd
from flask import Flask, redirect, url_for, request
import sys
from housing import Housing 

app = Flask(__name__)

@app.route('/housing',methods = ['POST', 'GET'])
def housing():
    if request.method == 'POST':
        
        list_var_str = []
        list_var = []

        list_var_str.append(request.form['nm1'])
        list_var_str.append(request.form['nm2'])
        list_var_str.append(request.form['nm3'])
        list_var_str.append(request.form['nm4'])
        list_var_str.append(request.form['nm5'])
        list_var_str.append(request.form['nm6'])
        list_var_str.append(request.form['nm7'])
        list_var_str.append(request.form['nm8'])
        list_var_str.append(request.form['nm9'])
        
        for var in list_var_str:
          if var:
            list_var.append(float(var))
          else:
            list_var.append(0)
            
        list_var.append(request.form['nm10'])
        n_kneighbors = request.form['n']

        if n_kneighbors:
          n_kneighbors = int(n_kneighbors)
        else:
          n_kneighbors = 5
        house1 = Housing()

        df = house1.findKneighbors(list_var, n_kneighbors)
        
        return df.to_html(header="true", table_id="table")
    else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = var_1))

if __name__ == '__main__':
   app.run(debug = True)