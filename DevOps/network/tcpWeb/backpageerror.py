# -*- coding:utf-8 -*-

# 返回指定页面存在的问题

"""
1.访问的页面不存在
  解决方案: 对打开文件的代码,做异常捕获.
2. 默认首页-直接访问地址:, 不加路径报错.
解决思路: 如果直接访问, 请求行中可以以"/"作为默认条件. 
"""


import socket
import os

indexpath = r"python-scripts\DevOps\network\tcpWeb\static"

def request_handler(new_client_socket,ip_port):
    """接收信息,并且做出响应"""
    # 7. 接收客户端浏览器发送的请求协议.
    request_data = new_client_socket.recv(1024)
    # print(request_data)
    # 8. 判断请求协议是否为空.
    if not request_data:
        print("{}客户端已经下线.".format(str(ip_port)))
        new_client_socket.close()
        return 

    # 根据客户端浏览器请求的资源路径,返回请求资源. 
    # 1) 把请求协议解码,得到请求报文的字符串
    request_text = request_data.decode()
    # 2) 得到请求行
    #  - 查找,第一个\r\n出现的位置.
    loc = request_text.find("\r\n")
    #  - 截取字符串,从开头嫁娶到第一个\r\n出现的位置.
    request_line = request_text[:loc]
    print(request_line)    
    #  - 把请求行,按照空格拆分, 得到列表.
    request_line_list = request_line.split(" ")
    print(request_line_list)

    # 得到请求的资源路径
    file_path = request_line_list[1]
    # print(file_path)
    print("{a}正在请求:{b}".format(a=str(ip_port),b=file_path))

    # 设置默认首页
    if file_path == "/":
        file_path = "/index.html"

    # 9. 拼接响应报文.
    # 9.1 响应行
    response_line = "HTTP/1.1 200 OK\r\n"
    # 9.2 响应头
    response_header = "Server:Python3-vscodeIDE/2.1\r\n"
    # 9.3 响应空行
    response_blank = "\r\n"
    # 9.4 响应主体
    try:
        # 返回固定页面, 通过with读取文件.
        with open(indexpath + file_path,"rb") as file:
            # 把读取的文件内容返回给客户端.
            response_body = file.read()
    except Exception as e:
        # 重新修改响应行为404
        response_line = "HTTP/1.1 404 Not Found\r\n"
        # 响应的内容为错误.
        response_body = "Error! {}".format(str(e))
        # 把内容转换为字节码
        response_body = response_body.encode()

    response_data = (response_line + response_header + response_blank).encode() + response_body

    # 10. 发送响应报文.
    new_client_socket.send(response_data)

    # 11. 关闭连接.
    new_client_socket.close()

def main():
    """主函数"""
    fix_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #3.设置地址重用,          当前套接字         地址重用
    fix_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    #4.绑定端口
    fix_socket.bind(("18.18.23.254",8822))
    # 5.设置监听, 让套接字由主动变为被动接收.
    fix_socket.listen(128)
    # 6.接受客户端连接.
    new_client_socket,ip_port = fix_socket.accept()
    # 调用功能函数处理请求并且响应
    request_handler(new_client_socket,ip_port)

    # 11 关闭操作
    fix_socket.close()

if __name__=="__main__":
    main()