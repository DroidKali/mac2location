#!/usr/bin/env python3
# 通过 WiFi MAC 地址查询对应的经纬度坐标获取实际地理位置
import click
import requests

@click.command()
@click.option('-a', '--address', help='指定要查询的MAC地址', prompt='请输入要查询的MAC地址', required=True)
def main(address):
    """
    通过 WiFi MAC 地址查询对应的经纬度坐标获取实际地理位置
    """
    try:
        resp = requests.get(f'http://api.cellocation.com:84/wifi/?mac={address}&output=json', timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        click.secho(f'请求或数据解析错误: {e}', fg='red', err=True)
        return
    
    if data.get('errcode') == 0:
        click.secho("查询结果:", fg='green')
        click.secho(f"经度: {data.get('lon', '')}", fg='green')
        click.secho(f"纬度: {data.get('lat', '')}", fg='green')
        click.secho(f"定位精确半径: {data.get('radius', '')}", fg='green')
        click.secho(f"详细地址: {data.get('address', '')}", fg='green')
    else:
        click.secho("暂无查询结果", fg='red')

if __name__ == "__main__":
    main()
