from flask import Flask ,render_template,request,redirect
import mysqlClass as mc

app = Flask(__name__)
@app.route("/",methods=("GET","POST"))
def index():
    sql1 = mc.sql(mc.config3)
    sql1.create_table(3)
    a = request.form.to_dict()
    print(a)
    if a != {}:
        topics = ''
        grade = ''
        name = a['username']
        content = list(a.keys())
        content.remove('username')
        if content == []:
            topics = '1234567'
            grade = '1234'
        else:
            content = "".join(content)
            if "g" not in content:
                grade = '1234'
                topics = content
            else:
                content=content.split(".")
                topics = content[0]
                if content[0] == '':
                    topics = '1234567'
                content.remove(content[0])
                content = "".join(content)
                content = content.split("g")
                content = "".join(content)
                grade = content
        print("YES")
        print(grade)
        print(topics)
        b = sql1.select_lines(3)
        namelist = []
        for i in b :
            namelist.append(i[0])
        # print(namelist,name,sep="\n")
        if name in namelist:
            return redirect("/sorry")
        tosql = [[name,topics,grade]]
        print(tosql)
        sql1.lines_insert(3,tosql)
        return redirect ("/welcome")
    return render_template("test.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/sorry")
def sorry():
    return render_template("sorry.html")
app.run(host = "0.0.0.0")