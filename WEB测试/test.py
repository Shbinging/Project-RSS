from flask import Flask ,render_template,request,redirect
import mysqlClass as mc

app = Flask(__name__)
@app.route("/",methods=("GET","POST"))
def index():
    sql1 = mc.sql(mc.config3)
    sql1.create_table(2)
    a = request.form.to_dict()
    #print(a)
    if a != {}:
        name = a['username']
        topics = list(a.keys())
        topics.remove('username')
        topics.sort()
        topics = "".join(topics)
        # print(name,topics)
        b = sql1.select_lines(2)
        namelist = []
        for i in b :
            namelist.append(i[0])
        # print(namelist,name,sep="\n")
        if name in namelist:
            return redirect("/sorry")
        tosql = [[name,topics]]
        print(tosql)
        sql1.lines_insert(2,tosql)
        return redirect ("/welcome")
    return render_template("test.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/sorry")
def sorry():
    return render_template("sorry.html")
app.run(host = "0.0.0.0")