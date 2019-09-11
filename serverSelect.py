# coding=utf-8
import urllib
import os
import time
import random
from websocket_server import WebsocketServer
import sys
import logging

# 因为考虑到传入的字符串有非英文字符，
# 所以手动设置编码，否则可能会报编码错误
reload(sys)
sys.setdefaultencoding('utf-8')


def findAllFiles(root_dir, filter):
    """
    在指定目录查找指定类型文件

    :param root_dir: 查找目录
    :param filter: 文件类型
    :return: 路径、名称、文件全路径

    """

    # print("Finding files ends with \'" + filter + "\' ...")
    separator = os.path.sep
    paths = []
    names = []
    files = []
    for parent, dirname, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(filter):
                paths.append(parent + separator)
                names.append(filename)
    for i in range(paths.__len__()):
        files.append(paths[i] + names[i])
    # print (names.__len__().__str__() + " files have been found.")
    paths.sort()
    names.sort()
    files.sort()
    return paths, names, files


def download():
    _, _, files = findAllFiles(".", "download.idx")
    if len(files) == 0:
        url = "http://zhaoxuhui.top/posts.idx"
        urllib.urlretrieve(url, "download.idx")
        # print "no file,download"
        return "download.idx"
    else:
        c_time = os.path.getmtime(files[0])
        n_time = time.time()
        if abs(n_time - c_time) > 86400:
            url = "http://zhaoxuhui.top/posts.idx"
            urllib.urlretrieve(url, "download.idx")
            # print "have file but expired,download"
            return "download.idx"
        else:
            # print "have file and not expired"
            return files[0]


def readFile(file_path):
    urls = []
    f = open(file_path, 'r')
    for item in f.readlines()[1:]:
        urls.append(item.decode('gb2312').encode('utf-8').strip())
    return urls


def select(urls):
    index = random.randint(0, len(urls) - 1)
    return "https://zhaoxuhui.top/blog/" + urls[index]


def new_client(client, server):
    # print "Time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("Client(%d) has joined." % client['id'])


def client_left(client, server):
    print("Client(%d) disconnected\n" % client['id'])


def message_back(client, server, message):
    # 这里的message参数就是客户端传进来的内容
    print("Client(%d) said: %s" % (client['id'], message))
    # 这里可以对message进行各种处理
    result = handle_login(message)
    # 将处理后的数据再返回给客户端
    server.send_message(client, result)


def handle_login(text):
    # 根据传入的参数处理
    if text == "randomRequest":
        url = select(readFile(download()))
        print "Return:", url
        return url
    else:
        print "error param"
        return "https://zhaoxuhui.top"


if __name__ == '__main__':
    server = WebsocketServer(4200, host='', loglevel=logging.INFO)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_back)
    server.run_forever()
