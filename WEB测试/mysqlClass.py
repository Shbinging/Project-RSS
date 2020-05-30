import mysql.connector


config1 = {
        'host': 'localhost',
        'port': 3306,
        'database': 'RSS',
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

config3={
        'host': 'localhost',
        'port': 3308,
        'database': 'RSS',
        'user': 'root',
        'password': 'njuRSS2019.',
        'charset': 'utf8',
        'use_unicode': True,
        'get_warnings': True,

}

configlinux={
        'host': 'localhost',
        'port': 3306,
        'database': 'RSS',
        'user': 'root',
        'password': 'njuRSS2019.',
        'charset': 'utf8',
        'use_unicode': True,
        'get_warnings': True,

}


create_order=[
(       "CREATE TABLE test ("
        "    id INT UNSIGNED NOT NULL AUTO_INCREMENT, "
        "    status INT NOT NULL DEFAULT 0 , "
        "    time VARCHAR(200) , "
        "    title VARCHAR(200) , "
        "    info LONGTEXT , "  
        "    url TEXT , "
        "    label TEXT , "
        "PRIMARY KEY (id))"
),

(       "CREATE TABLE raw_info ("
        "    id INT UNSIGNED NOT NULL AUTO_INCREMENT, "
        "    status INT NOT NULL DEFAULT 0 , "
        "    time VARCHAR(200) , "
        "    title VARCHAR(200) , "
        "    info LONGTEXT , "  
        "    url TEXT , "
        "    label TEXT , "
        "PRIMARY KEY (id))"
)
,

(       "CREATE TABLE user ("
        "    id INT UNSIGNED NOT NULL AUTO_INCREMENT, "
        "    username TEXT , "  
        "    topics TEXT , "
        "PRIMARY KEY (id))"
)
]

insert_order=[
"INSERT INTO test (time, title, info, url) VALUES (%s, %s, %s ,%s)",

"INSERT INTO test2 (time, title, info, url) VALUES (%s, %s, %s ,%s)",
#在这里输入插入语句，注意格式第一个括号里面是对应的栏目，后一个括号全部是%s
"INSERT INTO user (username , topics) VALUES (%s , %s)"
]

select_order=[
"SELECT title FROM test WHERE status = 0",

"SELECT title , time FROM test2 WHERE status = 0",

"SELECT username FROM user"
#在这里输入MySQL的SELECT语句
]

update_order=[
"UPDATE test SET status = %s WHERE id = %s",

"UPDATE test2 SET status = %s WHERE id = %s"
]

delete_order=[
"DELETE from test WHERE id = %s ",

"DELETE from test WHERE id = %s "
]


class sql:
    __cnx = 0
    __cur = 0
    def __init__(self,config):
        try:
            self.__cnx = mysql.connector.connect(**config)
            print("Connected")
        except:
            print("Failed to connect")
            exit(-1)
        self.__cur = self.__cnx.cursor()
    def create_table(self,ordernum):
        try:
            self.__cur.execute(create_order[ordernum])
            self.__cnx.commit()
            print("CREATE complete")
        except:
            print("Failed to create the table, or the table had been created")
    def lines_insert(self,ordernum,data):
        try:
            self.__cur.executemany(insert_order[ordernum],data)
            self.__cnx.commit()
            print("Insert complete")
        except:
            print("Failed to INSERT")
            # self.feedback()
            exit(-1)
    def select_lines(self,ordernum):
        try:
            output = []
            self.__cur.execute(select_order[ordernum])
            for row in self.__cur.fetchall():
                row = list(row)
                output.append(row)
            return output
        except:
            print("Failed to SELECT")
            exit(-1)
    def update(self,ordernum,data):
        try:
            self.__cur.executemany(update_order[ordernum],data)
            self.__cnx.commit()
            print("Update complete")
        except:
            print("Failed to update")
            exit(-1)
    def delete(self,ordernum,data):
        try:
            self.__cur.executemany(delete_order[ordernum],data)
            self.__cnx.commit()
        except:
            print("Failed to delete")


if __name__ == "__main__":
    sql1 = sql(config3)
    data = [['3','中文','3','4'],['3','4','5','6']]
    sql1.create_table(1)
    sql1.lines_insert(1,data)
   
    
   

        