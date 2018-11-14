#Sigursteinn Óli Þorsteinsson
#07/11/18
#Verkefni 7

#from sys import argv
import pymysql
from bottle import *


@get("/")
def index():
    return template("index")

@route('/donyskra', method='POST')
def nyr():
    u = request.forms.get("user")
    p = request.forms.get("pass")
    n = request.forms.get("nafn")

    conn = pymysql.connect(host="tsuts.tskoli.is", port=3306, user="1803012590", password="mypassword", db="1803012590_vef2_demo")
    cur = conn.cursor()

    cur.execute("SELECT count(*) FROM 1803012590_vef2_demo.users where user=%s",(u))
    result = cur.fetchone()

    if result[0] == 0:
        cur.execute("INSERT INTO 1803012590_vef2_demo.users Values(%s,%s,%s)", (u, p, n))
        conn.commit()
        cur.close()
        conn.close()
        return u, " hefur verið skráður <br><a href='/'>Heim</a>"
    else:
        return u, " er frátekið notendanafn, reyndu aftur <br><a href='/'#ny>Nýskrá</a>"

@route("/doinnskra", method="POST")
def doinn():
    u = request.forms.get("user")
    p = request.forms.get("pass")

    conn = pymysql.connect(host="tsuts.tskoli.is", port=3306, user="1803012590", password="mypassword", db="1803012590_vef2_demo")
    cur = conn.cursor()

    cur.execute("SELECT count(*) FROM 1803012590_vef2_demo.users where user=%s and pass=%s",(u,p))
    result = cur.fetchone()

    if result[0] == 1:
        
        cur.close()
        conn.close()
        return template("leyni.tpl",u=u)
    else:
        return template("ekkileyni.tpl")


@route("/members")
def member():
    conn = pymysql.connect(host="tsuts.tskoli.is", port=3306, user="1803012590", password="mypassword", db="1803012590_vef2_demo")
    c = conn.cursor()
    c.execute("SELECT nafn FROM users")
    result = c.fetchall()
    c.close
    output = template("members",rows=result)
    return output

@route("/static/<skra>")
def static_skra(skra):
    return static_file(skra, root="./static")

@error(404)
def villa(error):
    return "<h1 style = color:red>Þessi síða finnst ekki</h1>"


run(debug=True)
#run(host='0.0.0.0', port=os.environ.get('PORT'))

