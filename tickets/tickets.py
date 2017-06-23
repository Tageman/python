# coding=utf-8

"""命令行车票查询

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help  显示帮助
    -g         高铁
    -d         动车
    -t         特快
    -k         快速
    -z         直达
    
Example:
    tickets 北京 上海 2017-5-6
    tickets -dg 上海 南京 2017-6-6
"""
import json

import prettytable
import requests
from docopt import docopt
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from stations import stations

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    # 这里只有在stations 中含有的对应 date是没有对应的所以不需要stations.get
    from_stations = stations.get(arguments['<from>'])
    to_stations = stations.get(arguments['<to>'])
    date = arguments['<date>']
    # 创建url  查询API的url
    url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station" \
          "={}&leftTicketDTO.to_station={}&purpose_codes=ADULT".format(date, from_stations, to_stations)

    result = requests.get(url, verify=False)
    result = json.loads(result.text)
    # 解析返回值
    trains = []
    cr = result['data']['map']
    for result_str in result['data']['result']:
        cm = result_str.split('|')
        cq = {}
        cq['train_no'] = cm[2]
        cq['station_train_code'] = cm[3]
        cq['start_station_telecode'] = cm[4]
        cq['end_station_telecode'] = cm[5]
        cq['from_station_telecode'] = cm[6]
        cq['to_station_telecode'] = cm[7]
        cq['start_time'] = cm[8]
        cq['arrive_time'] = cm[9]
        cq['lishi'] = cm[10]
        cq['canWebBuy'] = cm[11]
        cq['yp_info'] = cm[12]
        cq['start_train_date'] = cm[13]
        cq['train_seat_feature'] = cm[14]
        cq['location_code'] = cm[15]
        cq['from_station_no'] = cm[16]
        cq['to_station_no'] = cm[17]
        cq['is_support_card'] = cm[18]
        cq['controlled_train_flag'] = cm[19]
        cq['gg_num'] = cm[20] if cm[20] else "--"
        cq['gr_num'] = cm[21] if cm[21] else "--"
        cq['qt_num'] = cm[22] if cm[22] else "--"
        cq['rw_num'] = cm[23] if cm[23] else "--"
        cq['rz_num'] = cm[24] if cm[24] else "--"
        cq['tz_num'] = cm[25] if cm[25] else "--"
        cq['wz_num'] = cm[26] if cm[26] else "--"
        cq['yb_num'] = cm[27] if cm[27] else "--"
        cq['yw_num'] = cm[28] if cm[28] else "--"
        cq['yz_num'] = cm[29] if cm[29] else "--"
        cq['ze_num'] = cm[30] if cm[30] else "--"
        cq['zy_num'] = cm[31] if cm[31] else "--"
        cq['swz_num'] = cm[32] if cm[32] else "--"
        cq['yp_ex'] = cm[33]
        cq['seat_types'] = cm[34]
        cq['from_station_name'] = cr[cm[6]]
        cq['to_station_name'] = cr[cm[7]]
        cs = {}
        cs['secretStr'] = cm[0]
        cs['buttonTextInfo'] = cm[1]
        cs['queryLeftNewDTO'] = cq
        trains.append(cs)

        table = prettytable.PrettyTable()
        table.field_names = ('车次', '车站', '时间', '历时', '商务座', '特等座',
                             '一等座', '二等座', '高级软卧', '软卧', '硬卧', '软座', '硬座', '无座', '其他')

    for train in trains:
        item = train['queryLeftNewDTO']

        table.add_row([
            item['station_train_code'],
            item['from_station_name'],
            item['start_time'],
            item['lishi'],
            item['swz_num'],
            item['tz_num'],
            item['zy_num'],
            item['ze_num'],
            item['gr_num'],
            item['rw_num'],
            item['yw_num'],
            item['rz_num'],
            item['yz_num'],
            item['wz_num'],
            item['qt_num']
        ])
        table.add_row(['', '\033[31m' + item['to_station_name'] + \
                       '\033[0m'] + ['' for _ in range(13)])
    print(table.get_string())


if __name__ == '__main__':
    cli()
