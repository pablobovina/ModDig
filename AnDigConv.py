# -*- coding: utf-8 -*-
from Usb import Usb
from Utils import msec_to_usec, nsec_to_usec, sec_to_usec, int_to_byte
import logging


class AnDigConv:
    usb = Usb()
    ad_ctrl = 0x0b
    ad_inter = 0x0c
    a_msb = 0x0a
    b_msb = 0x08
    ab_lsb = 0x09
    block = {0: ("000", 16), 1: ("001", 32), 2: ("010", 64), 3: ("011", 128),
             4: ("100", 256), 5: ("101", 512), 6: ("110", 1024), 7: ("111", 2048)}
    n_samples = 32

    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG,
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        pass

    def _modo(self, ctrl=0, adq=1, amo=0, rst=0 ):
        """
        :param ctrl: int
        :param adq: int
        :param amo: int
        :param rst:int
        :return: response
        """
        amo = self.blocks.get(amo, 1)
        self.n_samples = amo[1]

        cfg = str(rst) + amo[0] + "00" + str(adq) + str(ctrl)
        cfg = int(cfg, 2)
        data = ['r', chr(self.ad_ctrl), chr(cfg)]
        response = self.usb.request(data, 4)
        logging.info(response)
        return response

    def _status(self):
        data = ['S', chr(self.ad_ctrl), chr(0x00)]
        response = self.usb.request(data, 4)
        logging.info(response)
        return response

    def _interval(self, i, u):
        # 100ns  == 0.1us
        # N = intervalo / 100ns
        # ts = 255 - N

        d = {1: msec_to_usec(i), 2: nsec_to_usec(i), 3: sec_to_usec(i)}
        n = d / 0.1
        ival = 255 - n
        print ival
        data = ['t', chr(self.ad_inter), chr(ival)]
        response = self.usb.request(data, 4)
        logging.info(response)
        return response

    def _datatx(self, src, n):
        data = ['X', chr(src), chr(0x00)]
        response = self.usb.request(data, n)
        logging.info(response)
        return response

    def set_interval_samplin(self,i,u):
        return self._interval(i, u)


    def get_data_from_ad(self):

        ch_a = self._datatx(self.a_msb,self.n_samples)
        ch_b = self._datatx(self.b_msb,self.n_samples)
        ch_a_b = self._datatx(self.ab_lsb,self.n_samples)

        l_a = []
        l_b = []

        for i in range(self.n_samples):
            msb_a = int_to_byte(ord(ch_a[i]))[0]
            msb_b = int_to_byte(ord(ch_b[i]))[0]
            lsb_a = int_to_byte(ord(ch_a_b[i]))[0][4:8]
            lsb_b = int_to_byte(ord(ch_a_b[i]))[0][0:4]
            l_a.append(msb_a+lsb_a)
            l_b.append(msb_b+lsb_b)
