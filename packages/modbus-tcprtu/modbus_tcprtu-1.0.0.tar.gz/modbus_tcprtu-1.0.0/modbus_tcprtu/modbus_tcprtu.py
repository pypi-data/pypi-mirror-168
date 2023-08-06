# -*- coding: UTF-8 -*
'''
该模块用于兼容串口和以太网直传兼容
'''
from __future__ import print_function
from modbus_tk.modbus_tcp import call_hooks, TcpMaster, LOGGER, flush_socket, to_data, struct
from modbus_tk import utils


class TcpRtuMaster(TcpMaster):
    lasthead = b''

    def _send(self, request):
        """Send request to the slave"""
        retval = call_hooks("modbus_tcprtu.TcpRtuMaster.before_send", (self, request))
        if retval is not None:
            request = retval
        try:
            flush_socket(self._sock, 3)
        except Exception as msg:
            # if we can't flush the socket successfully: a disconnection may happened
            # try to reconnect
            LOGGER.error('Error while flushing the socket: {0}'.format(msg))
            self._do_open()
        # print('sraw', request)
        data = request[6:]  # 只取后面的数据部分
        # print('data', data)
        self.lasthead = request[0:4]  # 记录下去请求头
        crc = struct.pack(">H", utils.calculate_crc(data))
        req = data + crc  # 加上CRC
        # print('send', data)
        self._sock.send(req)

    def _recv(self, expected_length=-1):
        """
        Receive the response from the slave
        Do not take expected_length into account because the length of the response is
        written in the mbap. Used for RTU only
        """
        response = to_data('')
        length = 255
        while len(response) < length:
            rcv_byte = self._sock.recv(1)
            if rcv_byte:
                response += rcv_byte
                if len(response) == 3:
                    to_be_recv_length = struct.unpack(">BBB", response)[2]
                    length = to_be_recv_length + 3 + 2
            else:
                break
        retval = call_hooks("modbus_tcprtu.TcpRtuMaster.after_recv", (self, response))
        if retval is not None:
            return retval
        response = b'' + response
        # print('rraw', response)
        data = response[0:-2]  # 去掉CRC
        # print('data', data)
        lend = struct.pack(">H", len(data))  # 重新计算TCP的长度帧
        res = self.lasthead + lend + data  # 合成数据
        # print('recv', res)
        return res


if __name__ == '__main__':
    import time
    import modbus_tk.defines as cst

    # master = modbus_tcp.TcpMaster('192.168.1.2')
    # master = modbus_tcp.TcpMaster(host='io.inruan.com', port=9502)
    # master = TcpRtuMaster(host='127.0.0.1', port=9001)
    master = TcpRtuMaster(host='192.168.0.7', port=502)
    master.set_timeout(2)
    while True:
        print(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 124))
        # time.sleep(0.001)
