# -*- encoding: utf-8 -*-
import argparse
import yaml
import time
from zkw_db.my_db import Mysql
import logging
import json
import cv2


def read_yaml(yaml_dir: str):
    yaml_data = yaml.load(open(yaml_dir, 'r').read(), yaml.FullLoader)
    return yaml_data


def read_json():
    json_dir = './laugh.json'
    json_data = json.load(open(json_dir, 'r'))
    return json_data


def parse_opt():
    parse = argparse.ArgumentParser()
    parse.add_argument('--yaml_dir', type=str, help='config data_dir path', default='')
    parse.add_argument('--log_dir', type=str, help='save lod dir path', default='')
    args = parse.parse_args()
    return args


def main():
    # star_time = time.time()
    star_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print('start_time:', star_time)
    opts = parse_opt()
    json_data = read_json()
    yaml_dir = opts.yaml_dir = json_data['yaml_dir']
    log_dir = opts.log_dir = json_data['log_dir']
    config = read_yaml(yaml_dir=yaml_dir)

    # log日志信息
    logger = logging.getLogger('results')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_dir)
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
    print(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    '''
    数据库连接 
    '''
    my_db = Mysql(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database'],
        port=config['port'],
        charset=config['charset']
    )

    '''
    字典(dict)方式传参
    '''
    data = {
        'host': config['host'],
        'user': config['user'],
        'password': config['password'],
        'port': config['port'],
        'datetime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    }
    # 增
    sql = "INSERT INTO " + config['first_table'][0] + \
          "(host,user,password,port,datetime) VALUES ('%s','%s','%s','%s','%s') " \
          % (data['host'], data['user'], data['password'], data['port'], data['datetime'])
    logger.info(sql)
    my_db.insert(sql=sql)

    # #查询一条信息
    # sql = "select * from "+config['first_table']+" where age='17';"
    # logger.info(sql)
    # res = my_db.fetchone(sql)
    # print(res)
    #
    #
    # #改
    # sql = "update "+config['first_table']+" set age='18' where age='17';"
    # logger.info(sql)
    # my_db.updata(sql)
    #
    # #删
    # sql = "delete from "+config['first_table']+" where age='18';"
    # logger.info(sql)
    # my_db.updata(sql)
    #
    # #查询全部信息
    # sql = "select * from "+config['first_table']+" ;"
    # logger.info(sql)
    # for i in my_db.fetchall(sql):
    #     print(i)


if __name__ == '__main__':
    main()
