import pymysql


class Mysql:
    # 打开数据库的连接
    def __init__(self, host, user, password, database, port, charset):
        try:
            self.db = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port,
                charset=charset,
            )
        except pymysql.Error as e:
            print('数据库连接失败', e)
            exit()
        self.cursor = self.db.cursor()  # 创建一个游标对象

    # 查询一条信息
    '''
    sql = "select * from "+config['first_table']+" where age='17';"
    '''

    def fetchone(self, sql):
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            return data
        except pymysql.Error as e:
            print('fetchone Error', e)
            print('sql:', sql)

    # 查询全部信息
    '''
    sql = "select * from "+config['first_table']+" ;"
    for i in my_db.fetchall(sql):
        print(i)
    '''

    def fetchall(self, sql):
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        except pymysql.Error as e:
            print('fetchall Error:', e)
            print('sql :', sql)

    # 插入信息
    '''
    sql = "insert into " + config['first_table'] + "(id,name,age,hobby) values('1','aa','15','乒乓') "
    sql = "INSERT INTO " + config['first_table'] + "(host,user,password,port,datetime) VALUES ('%s','%s','%s','%s','%s') " % (data['host'], data['user'], data['password'],data['port'], data['datetime'])
    '''

    def insert(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except pymysql.Error as e:
            print('insert Error:', e)
            print('sql:', sql)

    # 修改或删除信息
    '''
    删  sql = "delete from "+config['first_table']+" where age='18';"
    改  sql = "update "+config['first_table']+" set age='18' where age='17';"
    '''

    def updata(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except pymysql.Error as e:
            print('updata Error:', e)
            print('sql:', sql)

    # 关闭游标 关闭数据库
    def close(self):
        self.cursor.close()
        self.db.close()
