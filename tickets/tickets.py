# coding: utf-8

"""命令行火车票查看器

Usage:
    tickets [-dgktz] <from> <to> <date>

Options:
    -h, --help 查看帮助
    -d         动车
    -g         高铁
    -k         快速
    -t         特快
    -z         直达

Examples:
    tickets 上海 北京 2016-10-10
    tickets -dg 成都 南京 2016-10-10
"""

import requests
from docopt import docopt
import json
from stations import stations


def cli():
    """Command-line interface"""
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    url = ('https://kyfw.12306.cn/otn/lcxxcx/query?' 
           'purpose_codes=ADULT&queryDate={}&' 
           'from_station={}&to_station={}').format(
                date, from_station, to_station
           )

    r = requests.get(url, verify=False)
    print(r.json())

if __name__ == '__main__':
    cli()
