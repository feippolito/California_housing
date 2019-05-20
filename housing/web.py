import pandas as pd
from flask import Flask, redirect, url_for, request
import sys
from housing import Housing
import io, csv

app = Flask(__name__)
house1 = Housing()

@app.route('/housing',methods = ['POST', 'GET'])
def housing():
    if request.method == 'POST':

        list_var_str = []
        list_var = []
        user_id = []

        user_id.append(request.form['name'])
        user_id.append(request.form['email'])

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

        #append to user_data csv file
        ## == python function ==
        #house1.appendTocsv(user_id, list_var, n_kneighbors )
        
        n_kneighbors_list = [n_kneighbors]
        user_data = user_id + list_var + n_kneighbors_list + ['\n']
        
        user_data_str = ','.join(map(str, user_data))
        
        fd = open(r"..\housing\user_data.csv", "a")
        fd.write(user_data_str)
        fd.close()
        
        #return nearest neighbors dataframe
        df = house1.findKneighbors(list_var, n_kneighbors)
        #transform dataframe to html
        return df.to_html(header="true", table_id="table")


if __name__ == '__main__':
    app.run(debug = True)