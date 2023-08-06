#!/bin/python3
#
# Copyright (c) 2022 北京实耐固连接技术有限公司,Inc.All rights reserved. 
#
# File Name:        mqtt_client.py
# Author:           Liu Fengchen <fengchen.liu@sng.com.cn>
# Created:          2022/9/13 周二
# Description:      包装mqtt的客户端类，开发者可直接调用。
import socket
import types
from ssl import SSLCertVerificationError
import paho.mqtt.client as mc
from . import general


class MQTTClient:
    def __init__(self, conf, log):
        self.__conf = conf
        self.__log = log
        self.__name = conf["client_id"]
        self.__client = mc.Client(client_id=self.__name)
        self.__client.username_pw_set(username=conf["username"], password=conf["password"])

        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message
        self.__client.on_publish = self.__on_publish
        self.__client.on_subscribe = self.__on_subscribe

        self.__message_event = None
        self.__connect_event = None
        self.__disconnect_event = None
        self.__publish_event = None
        self.__subscribe_event = None

        if conf["tls_enable"]:
            self.__client.tls_set(
                ca_certs=general.parse_path(conf["TSL"]["ca_certs"]),
                certfile=general.parse_path(conf["TSL"]["cert_file"]),
                keyfile=general.parse_path(conf["TSL"]["key_file"]),
                tls_version=mc.ssl.PROTOCOL_TLSv1_2
            )
            self.__client.tls_insecure_set(True)

    def set_connect_event(self, function):
        """
        设置连接事件的回调函数。

        函数原型：
            callback_function(client, userdata, flags, rc)

        回调函数参数:
            client:   此次回调的客户端实例。
            userdata: 在 Client() 或 set_userdata() 中设置的私有用户数据。
            flags:    代理发送的响应标志。
            rc:       连接结果

        flags 是包含来自broker的响应标志的字典：
            flags['session present'] - 此标志只对于将 clean session 设置为 0 的客户端有用。如果具有 clean session=0 的客户机
            重新连接到它以前连接到的broker，则此标志表示broker是否仍具有该客户机的会话信息。如果为 1，则会话仍然存在。

        rc 值的含义:
            0: 连接成功
            1: 连接失败 - 协议版本不正确
            2: 连接失败 - 无效的客户端标识符
            3: 连接失败 - 服务器不可用
            4: 连接失败 - 用户名或密码错误
            5: 连接失败 - 未授权
            6-255: 保留项
            详细的错误代码信息可参考https://www.vtscada.com/help/Content/D_Tags/D_MQTT_ErrMsg.htm

        :param function: 回调函数。
        """
        assert isinstance(function, types.FunctionType), "argument mast be a function"
        self.__connect_event = function

    def set_disconnect_event(self, function):
        """
        设置连接断开事件的回调函数。

        函数原型：
            callback_function(client, userdata, rc)

        回调函数参数:
            client:   此次回调的客户端实例。
            userdata: 在 Client() 或 set_userdata() 中设置的私有用户数据。
            rc:       连接断开原因。

        rc 值的含义:
            若该值为0，表示用户主动断开，其他任何值表示错误。
            详细的错误代码信息可参考https://www.vtscada.com/help/Content/D_Tags/D_MQTT_ErrMsg.htm

        :param function: 回调函数。
        """
        assert isinstance(function, types.FunctionType), "argument mast be a function"
        self.__disconnect_event = function

    def set_message_event(self, function):
        """
        设置连接断开事件的回调函数。

        函数原型：
            callback_function(client, userdata, message)

        回调函数参数:
            client:   此次回调的客户端实例。
            userdata: 在 Client() 或 set_userdata() 中设置的私有用户数据。
            message:  收到的消息内容。类型为 MQTTMessage。
                      该类的成员包括 topic, payload, qos, retain。

        :param function: 回调函数。
        """
        assert isinstance(function, types.FunctionType), "argument mast be a function"
        self.__message_event = function

    def set_publish_event(self, function):
        """
        设置发布消息事件的回调函数。

        函数原型：
            callback_function(client, data, mid)

        回调函数参数:
            client:   此次回调的客户端实例。
            userdata: 在 Client() 或 set_userdata() 中设置的私有用户数据。
            mid:      匹配从相应的 publish() 调用返回的中间变量，以允许跟踪传出消息。

        :param function: 回调函数。
        """
        assert isinstance(function, types.FunctionType), "argument mast be a function"
        self.__publish_event = function

    def set_subscribe_event(self, function):
        """
        设置订阅主题事件的回调函数。

        函数原型：
            callback_function(client, userdata, mid, granted_qos）

        回调函数参数:
            client:      此次回调的客户端实例。
            userdata:    在 Client() 或 set_userdata() 中设置的私有用户数据。
            mid:         匹配从相应的 publish() 调用返回的中间变量，以允许跟踪传出消息。
            granted_qos: 整数列表，这些整数提供代理为每个不同订阅请求授予的 QoS 级别。

        :param function: 回调函数。
        """
        assert isinstance(function, types.FunctionType), "argument mast be a function"
        self.__subscribe_event = function

    def set_userdata(self, data):
        """
        设置用户数据，该数据将可以从回调函数中获得。

        :param data: 要设置的数据。
        """
        self.__client.user_data_set(data)

    def connect(self):
        """
        根据构造函数传入的配置，向broker发起连接请求。若失败则打印错误日志。

        :return 0表示连接成功，非零表示连接失败。
        """
        serverstr = str(self.__conf['broker']['ip']) + ":" + str(self.__conf['broker']['port'])
        try:
            self.__client.connect(
                host=self.__conf["broker"]["ip"],
                port=self.__conf["broker"]["port"]
            )
            return 0
        except ConnectionError as error:
            self.__log.error(f"MQTT连接失败 ({serverstr}): {error.strerror} [Errno:{error.errno}]")
            return 1
        except socket.timeout:
            self.__log.error(f"MQTT连接超时 ({serverstr})")
            return 1
        except SSLCertVerificationError as error:
            self.__log.error(f"MQTT证书错误({serverstr}): {error.strerror} [Errno:{error.errno}]")
            return 1
        except socket.gaierror:
            self.__log.error(f"服务器名称或ip无效({serverstr}): 请检查配置文件是否正确！")

    def disconnect(self):
        """
        主动和broker断开连接。
        """
        self.__client.disconnect()

    def __on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.__log.info(f"{self.__name} 连接成功")
        else:
            self.__log.error(f"{self.__name} 连接失败")
        if self.__connect_event is not None:
            self.__connect_event(client, userdata, flags, rc)

    def __on_message(self, client, userdata, message):
        msg = message.payload.decode("utf-8")
        self.__log.debug(f"收到来自主题 {message.topic} 的消息(长度: {len(msg)}):\n"
                         f"------------------Message Content------------------\n"
                         f"{msg}\n"
                         f"---------------------------------------------------")
        if self.__message_event is not None:
            self.__message_event(client, userdata, message)

    def __on_publish(self, client, data, result):
        self.__log.debug(f"发布数据完成(mid: {result})")
        if self.__publish_event is not None:
            self.__publish_event(client, data, result)

    def __on_disconnect(self, client, userdata, rc):
        if rc == 0:
            self.__log.warring(f"MQTT已断开连接")
        elif rc == 4:
            self.__log.error("MQTT用户名或密码错误")
        elif rc == 5:
            self.__log.error("MQTT无权访问")
        elif rc == 7:
            self.__log.error("MQTT等待来自服务器的相应超时")
        else:
            self.__log.error(f"MQTT意外的断开连接 ({rc})")
        if self.__disconnect_event is not None:
            self.__disconnect_event(client, userdata, rc)

    def __on_subscribe(self, client, userdata, mid, rc):
        if self.__subscribe_event is not None:
            self.__subscribe_event(client, userdata, mid, rc)

    def subscribe(self, topic,  qos=0):
        """
        订阅主题。

        :param topic: 要订阅的topic字符串。
        :param qos: 设置qos等级，默认为0。
        """
        self.__client.subscribe(topic=topic, qos=qos)

    def publish(self, msg, topic=None):
        """
        发布消息。

        :param msg: 要发布的消息。
        :param topic: 目标topic字符串。
        :return 返回 MQTTMessageInfo 类的实例，可使用 info.is_published() 判断是否已经发送，
                也可使用 info.wait_for_publish() 阻塞等待至发送完成。publish() 调用的消息 ID
                和返回代码分别为 info.mid 和 info.rc。
        """
        ret = self.__client.publish(topic, msg)
        return ret

    def start(self):
        """
        为mqtt创建一个新线程并执行。

        :return 返回0表示一切正常，否则表示失败。
        """
        rc = self.__client.loop_start()
        if rc == mc.MQTT_ERR_INVAL:
            return rc
        else:
            return 0

    def stop(self):
        """
        将mqtt所在的线程以及其中的任务停止。

        :return: 返回0表示一切正常，否则表示失败。
        """
        rc = self.__client.loop_stop()
        if rc == mc.MQTT_ERR_INVAL:
            return rc
        else:
            return 0

