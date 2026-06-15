from flask import Flask, render_template, request, redirect, url_for, jsonify
from Controller.UserApi import *
from Controller.IndexAPI import SystemInfo
from Controller.BadyApi import bady_api
from Controller.promotionApi import promotion_api
from Controller.orderApi import order_api
from Controller.analysisApi import analysis_api
from Controller.dashboardApi import dashboard_api
from flask_cors import CORS

app = Flask(__name__, 
    static_folder='static',  # 指定静态文件夹路径
    template_folder='templates'  # 指定模板文件夹路径
)
CORS(app)
# app.register_blueprint(dapin_api, url_prefix='/dapin')
# app.register_blueprint(data_api, url_prefix='/data')
app.register_blueprint(user_api, url_prefix='/user')
# app.register_blueprint(admin_api, url_prefix='/admin')
# app.register_blueprint(sql_api, url_prefix='/sql')
app.register_blueprint(order_api, url_prefix='/api')
app.register_blueprint(bady_api, url_prefix='/api')
app.register_blueprint(promotion_api, url_prefix='/api')
app.register_blueprint(analysis_api, url_prefix='/api')
app.register_blueprint(dashboard_api)



@app.route('/')
def hello_world():  # put application's code here
    return render_template("page-login.html")


@app.route('/Index')
def Home():  # put application's code here
    return render_template("Index.html")
@app.route('/User')
def User():  # put application's code here
    return render_template("userlist.html")

@app.route('/Admin')
def Admin():  # put application's code here
    return render_template("adminlist.html")
@app.route('/register')
def register():
    return render_template("page-register.html")


@app.route('/badylist')
def badylist():
    return render_template('badylist.html')

@app.route('/promotionlist')
def promotionlist():
    return render_template('promotionlist.html')

@app.route('/orderlist')
def orderlist():
    return render_template('orderlist.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/system_info')
def system_info():
    return jsonify(SystemInfo.get_system_info())

if __name__ == '__main__':
    app.run(debug=True)

