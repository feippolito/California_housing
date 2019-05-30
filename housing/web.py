import pandas as pd
from flask import Flask, redirect, url_for, request
import sys
from housing import Housing
import io, csv

from flask_cors import CORS

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    """Decorator function that allows crossdomain requests.
      Courtesy of
      https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    # use str instead of basestring if using Python 3.x
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    # use str instead of basestring if using Python 3.x
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """
        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


app = Flask(__name__)
CORS(app)
house1 = Housing()

@app.route('/housing',methods = ['POST', 'GET'])
def housing():
    if request.method == 'POST':

        list_var_str = []
        list_var = []
        user_id = []

        user_id.append(request.values['name'])
        user_id.append(request.values['email'])

        list_var_str.append(request.values['nm1'])
        list_var_str.append(request.values['nm2'])
        list_var_str.append(request.values['nm3'])
        list_var_str.append(request.values['nm4'])
        list_var_str.append(request.values['nm5'])
        list_var_str.append(request.values['nm6'])
        list_var_str.append(request.values['nm7'])
        list_var_str.append(request.values['nm8'])
        list_var_str.append(request.values['nm9'])
        
        for var in list_var_str:
          if var:
            list_var.append(float(var))
          else:
            list_var.append(0)
            
        list_var.append(request.values['nm10'])
        n_kneighbors = request.values['n']

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
        #return "OK"

if __name__ == '__main__':
    app.run(debug = True)