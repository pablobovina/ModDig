# -*- coding: utf-8 -*-
from Usb import Usb
import logging


class ProgPul:
    usb = Usb()
    reg_ctrl = 0x50
    reg_inter = 0x51
    reg_transf = 0x52

    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG,
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    def _modo(self, mode):
        """
         reset: ['R'][direccion pp2_control][0x02]
         carga: ['c'][direccion pp2_control][0x03]
         micro: ['M'][direccion pp2_control][0x00]
         disparo: ['D'][direccion pp2_control][0x80]
         status: ['E'][direccion pp2_control][0x00]
        """

        mode = {0: ('R', chr(0x02)), 1: ('c', chr(0x03)), 2: ('M', chr(0x00)), 4: ('D', chr(0x80)),
                5: ('E', chr(0x00))}.get(mode, ('E', chr(0x00)))
        data = [mode[0], chr(self.reg_ctrl), mode[1]]
        response = self.usb.request(data, 4)
        logging.info(response)
        return response

    def _store_cmd(self, cmd):
        """
        guarda cmd en registro intermedio
         ['A'][direccion pp2_int][cmd]
        """
        data = ['A', chr(self.reg_inter), chr(cmd)]
        response = self.usb.request(data, 4)
        logging.info(response)
        return response

    def _update(self):
        """
        transfiere el comando del registro intermedio a la memoria
        ['T'][direccion pp2_trans][0x00]
        """
        data = ['T', chr(self.reg_transf), chr(0x00)]
        response = self.usb.request(data, 4)
        logging.info(response)
        return response
