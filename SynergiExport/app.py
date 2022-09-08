from flask import Flask
from flask import Flask, render_template, request
import SingleSiteMoveForSynergiPipeline
import requests
import os

app = Flask(__name__)
@app.route('/')
def main():
    return render_template("mainPage.html")
@app.route("/forward", methods=['GET'])
def main_get():
    return render_template("mainPage.html")
@app.route("/forward", methods=['POST'])
def main_post():
    username = request.form['UserName']
    password = request.form['Password']
    scr = request.form['script'] + '/api'
    path = "\\\\ume7001\\UME_Common\\Common\\" + request.form['SavingPath']
    s = requests.Session()
    payload = {"username": username, "password": password}
    try:
        response = s.post(scr + '/login',json=payload)
        code = response.status_code
        print(code)
        if code == 200:
            if os.path.isdir(path):
                try:
                    SingleSiteMoveForSynergiPipeline.synergi_function(username,password, scr, path)
                    return render_template("mainPage.html", result = "Success, export complete", status = 1)
                except:
                    return render_template("mainPage.html", result = "You have no authorization to this site", status = 5)
            return render_template("mainPage.html", result = "Error: Invalid saving path", status = 2)
        return render_template("mainPage.html", result = "Error: Check your username or password", status = 3)
    except Exception as e:   
        return render_template("mainPage.html", result = "This URL is invalid", status = 4)

if __name__ == '__main__':
    app.run(debug=True)