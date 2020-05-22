import mysql.connector


config1 = {
        'host': 'localhost',
        'port': 3306,
        'database': 'test',
        'user': 'root',
        'password': 'abc@123',
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
     "CREATE TABLE test ("
        "    id INT UNSIGNED NOT NULL AUTO_INCREMENT, "
        "    status INT NOT NULL DEFAULT 0 , "
        "    time VARCHAR(200) , "
        "    title VARCHAR(200) , "
        "    info LONGTEXT , "  
        "    url TEXT , "
        "    label TEXT , "
        "PRIMARY KEY (id))"
)

insert_order = "INSERT INTO test (time, title, info, url) VALUES (%s, %s, %s ,%s)"
#在这里输入插入语句，注意格式第一个括号里面是对应的栏目，后一个括号全部是%s

select_order = "SELECT title FROM test WHERE id IN (1,2,3,4,5,6)"
#在这里输入MySQL的SELECT语句

update_order = "UPDATE test SET status = %s WHERE id = %s"

delete_order = "DELETE from test WHERE id = %s "


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
    def create_table(self):
        try:
            self.__cur.execute(create_order)
            self.__cnx.commit()
            print("CREATE complete")
        except:
            print("Failed to create the database")
            exit(-1)
    def lines_insert(self,insert_oder, data):
        try:
            self.__cur.executemany(insert_order,data)
            self.__cnx.commit()
            print("Insert complete")
        except:
            print("Failed to INSERT")
            # self.feedback()
            exit(-1)
    def select_lines(self,select_order):
        try:
            output = []
            self.__cur.execute(select_order)
            for row in self.__cur.fetchall():
                output.append(row)
            return output
        except:
            print("Failed to SELECT")
            exit(-1)
    def update(self,update_order, data):
        try:
            self.__cur.executemany(update_order,data)
            self.__cnx.commit()
            print("Update complete")
        except:
            print("Failed to update")
            exit(-1)
    def delete(self,delete_order, data):
        try:
            self.__cur.executemany(delete_order,data)
            self.__cnx.commit()
        except:
            print("Failed to delete")


if __name__ == "__main__":
    sql1 = sql(config1)
    result = sql1.select_lines("SELECT title FROM test WHERE id IN (1,2,3,4,5,6)");
    print(result);
   

        