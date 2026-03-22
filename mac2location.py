#!/usr/bin/env python3
# 通过MAC地址查询对应的经纬度坐标获取实际地理位置
import click
import requests

@click.command()
@click.option('-a', '--address', help='指定要查询的MAC地址', prompt='请输入要查询的MAC地址', required=True)
def main(address):
    resp = requests.get(f'http://api.cellocation.com:84/wifi/?mac={address}&output=json')
    if resp.json().get('errcode') == 0:
        print('查询结果:')
        print(f'经度: {resp.json().get('lon', '')}')
        print(f'纬度: {resp.json().get('lat', '')}')
        print(f'定位精确半径: {resp.json().get('radius', '')}')
        print(f'详细地址: {resp.json().get('address', '')}')
    else:
        print('暂无查询结果')

if __name__ == "__main__":
    main()
