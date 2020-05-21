import mysql.connector


config1 = {
        'host': 'localhost',
        'port': 3306,
        'database': 'comp',
        'user': 'root',
        'password': 'wsy20000812',
        'charset': 'utf8',
        'use_unicode': True,
        'get_warnings': True,
    }

config2={
    'host': 'localhost',
        'port': 3306,
        'database': 'user',
        'user': 'root',
        'password': 'wsy20000812',
        'charset': 'utf8',
        'use_unicode': True,
        'get_warnings': True,
}

create_order = (
     "CREATE TABLE names2 ("
        "    id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT, "
        "    name VARCHAR(30) DEFAULT 'AAA' NOT NULL, "
        "    info TEXT , "  
        "    age TINYINT UNSIGNED DEFAULT '30', "
        "PRIMARY KEY (id))"
)

insert_order = "INSERT INTO names2 (name, info, age) VALUES (%s, %s, %s)"
#在这里输入插入语句，注意格式第一个括号里面是对应的栏目，后一个括号全部是%s

select_order = "SELECT id, name, info, age FROM names2 ORDER BY id"
#在这里输入MySQL的SELECT语句


class sql:
    _cnx = 0
    _cur = 0
    def __init__(self,config):
        try:
            self._cnx = mysql.connector.connect(**config)
            print("Connected")
        except:
            print("Failed to connect")
            exit(-1)
        self._cur = self._cnx.cursor()
    def create_table(self):
        try:
            self._cur.execute(create_order)
            # self._cnx.commit()
            print("CREATE complete")
        except:
            print("Failed to create the database")
            exit(-1)
    def lines_insert(self,data):
        try:
            self._cur.executemany(insert_order,data)
            self._cnx.commit()
            print("Insert complete")
        except:
            print("Failed to INSERT")
            # self.feedback()
            exit(-1)
    def select_lines(self):
        try:
            output = []
            self._cur.execute(select_order)
            for row in self._cur.fetchall():
                output.append(row)
            return output
        except:
            print("Failed to SELECT")
            exit(-1)


if __name__ == "__main__":
    sql1 = sql(config1)
    info = "abc"
    data = [['Geert', info, 30], ['Jan', info, 31], ['Michel', info, 32]]
    sql1.lines_insert(data)
    result = sql1.select_lines()
   

        