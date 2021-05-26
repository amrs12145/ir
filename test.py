

from flask import Flask,redirect,url_for,request

app = Flask(
    __name__
)


@app.route('/home')
def fun1():
    return 'home/test'
@app.route('/test')
def fun2():
    return 'test'
@app.route('/home/h/test/<name>')
def fun3(name):
    return 'home/h/test =>' + name


@app.route('/',methods=['POST','GET'])

def local():
    if request.method=='POST':
        user = request.form['btn']
        return redirect(url_for('fun3',name='amr'))
    else :
        user= request.args.get('btn2')
        return 'GET request ' + user




if __name__ == '__main__':
    app.run()