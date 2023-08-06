#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pymysql
def return_sql_info(host,user,passwd,port,sql):
    conn = pymysql.connect(host=host, user=user, passwd=passwd, port=int(port))
    # 获取游标
    global result
    cursor = conn.cursor()
    try:
        # 查询数据
        # print sql
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        conn.rollback()  # 事务回滚
        print('事务处理失败{}'.format(e))
    else:
        conn.commit()  # 事务提交
        # print '事务处理成功'
    cursor.close()  # 先关闭游标
    conn.close()  # 再关闭数据库连接
    # print result
    return result


def return_sql_info_data(host,user,passwd,port,database,sql):
    conn = pymysql.connect(host=host, user=user, passwd=passwd,database=database, port=int(port))
    # 获取游标_test22
    global result
    cursor = conn.cursor()
    try:
        # 查询数据
        # print sql
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        conn.rollback()  # 事务回滚
        print(database)
        print('事务处理失败{}'.format(e))
    else:
        conn.commit()  # 事务提交
        # print '事务处理成功'
    cursor.close()  # 先关闭游标
    conn.close()  # 再关闭数据库连接
    # print result
    return result
def test():
    print("test succeed!!!")