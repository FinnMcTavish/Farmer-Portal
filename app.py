from flask import Flask, render_template, request
import os
from selecterSQL import PSelectSql
from inserterSQL import InsertSql
from textspeech import speaker
from updaterSQL import UpdateSql
from buyerUpdate import BUpdateSql

# chennai - vellore 10
# vellore - bangalore 20
# chennai - bangalore 30

UPLOAD_FOLDER = 'C:\#Dev\ImagineCup\ImagesML'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__,template_folder='template')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

pred = 111
grade = 'U'
Uname = ""

@app.route('/')
def index():
    rec1 = PSelectSql()
    loc1 = "chennai"
    loc2 = "vellore"
    loc3 = "bangalore"
    return render_template('BuySell.html',rec1 = rec1 , pri = loc1 , vel = loc2 , bang = loc3 )

@app.route('/vellore/')
def vellore():
    rec1 = PSelectSql()
    loc1 = "chennai"
    loc2 = "vellore"
    loc3 = "bangalore"
    return render_template('BuySellvel.html',rec1 = rec1 , chen = loc1,pri = loc2,bang=loc3)

@app.route('/bangalore/')
def bangalore():
    rec1 = PSelectSql()
    loc1 = "chennai"
    loc2 = "vellore"
    loc3 = "bangalore"
    return render_template('BuySellbang.html',rec1 = rec1 , chen = loc1,vel=loc2,pri=loc3)

@app.route('/farmer')
def farmer():
    return render_template('farmer.html')

@app.route('/uploader/', methods = ['GET', 'POST'])
def upload_file():
      f = request.files['file']
      n = request.form['name']
      global Uname
      Uname = n
      fr = n + ".jpeg"
      l = request.form['loc']
      w = request.form['weight']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], fr))
      # grade = functioncall(fr)
      # pred = calculate cost as grade * weight
      tup =(n,l,grade,pred, w,'NULL','NULL',0,0)
      InsertSql(tup)
      speaker("Thankyou for Choosing Our Service" + n)
      return render_template('confirm.html',name=n , loc=l, weight=w, cost = pred, grade=grade)

@app.route('/final/', methods = ['GET', 'POST'])
def final_file():
    speaker('Thankyou for selecting Predicted Value')
    return 'Thankyou for selecting Predicted Value'

@app.route('/finalown/', methods = ['GET', 'POST'])
def finalown_file():
    c = request.form['cost']
    UpdateSql(c,Uname)
    speaker('Thankyou for giving your own value')
    return 'Thankyou for giving your own value'

@app.route('/done/', methods = ['GET', 'POST'])
def done():
    n = request.form['name']
    b = request.form['loca']
    fn = request.form['fname']
    t = request.form['total']
    l = request.form['log']
    BUpdateSql(n,b,l,t,fn)
    return 'Thankyou for booking the crop'
if __name__ == '__main__':
   app.run(debug = True)


   