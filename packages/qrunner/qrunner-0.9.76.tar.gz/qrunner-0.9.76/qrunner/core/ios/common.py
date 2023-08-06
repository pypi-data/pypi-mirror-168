import os
import socket


def get_device_list():
    """获取当前连接的设备列表"""
    cmd = 'tidevice list'
    output = os.popen(cmd).read()
    device_list = [item.split(' ')[0] for item in output.split('\n') if item]
    return device_list


def get_tcp_port(udid: str):
    """获取可用端口号"""
    # tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # tcp.bind(("", 0))
    # _, port = tcp.getsockname()
    # tcp.close()
    port = int(udid.split('-')[0])
    return port


if __name__ == '__main__':
    print(get_device_list())

