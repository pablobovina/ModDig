# -*- coding: utf-8 -*-
from Usb import Usb
from Utils import int_to_byte, bytes_to_reg, bytes_reg_to_int_reg
import logging


class SintDigFrec:
    usb = Usb()
    reg1 = [0x04, 0x05, 0x06, 0x07, 0x08, 0x09]
    reg2 = [0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F]
    dds_cmd = 0x70
    dds_mode = 0x71
    dds_rst = 0x72
    dds_test = 0x73
    dds_ram = 0x74
    dds_reg = 0x75
    dds_udclk = 0x76
    dds_code = 0x77
    dds_data = 0x78
    base_freq = 281474976710656
    fmlclk = 3000000000

    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG,
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        return
    
    def _reset(self):
        """ ['a']
            [direccion dds2_rst]
            [0x00]
        """

        data = ['b', chr(self.dds_mode), chr(0x00)]
        response = self.usb.request(data, 4)
        logging.info(response)

        data = ['a', chr(self.dds_rst), chr(0x00)]
        response = self.usb.request(data, 4)
        logging.info(response)

        return
    
    def _modo(self, mode):
        """ ['b']
            [dirección dds2_control]
            [modo]
        000 = 0 carga de frecuencia / modo PC 0x00
        010 = 1 carga de fases 0x02
        101 = 2 modo dds con transferencia  de fases 0x05
        """

        mode = {0: chr(0x00), 1: chr(0x02), 2: chr(0x05)}.get(mode, chr(0x00))
        data = ['b', chr(self.dds_mode), mode]
        response = self.usb.request(data, 4)
        logging.info(response)
        return response
    
    def _load(self, reg1, addr, reg2, dat):
        """ ['k']
            [reg. de dir. intermedio]
            [dir. del reg. del DDS2]
            [reg. de dato intermedio]
            [dato]
        """

        data = ['k', chr(reg1), chr(addr), chr(reg2), chr(dat)]
        response = self.usb.request(data, 4)
        logging.info(response)
        return response
    
    def _load_phase(self, reg, addr1, reg2, dath, addr2, datl):
        """ ['w']
            [reg.dirección dds2_ram]
            [dirección]
            [dirección reg.dds2_dato]
            [dato_h]

            [reg.dirección dds2_ram]
            [dirección + 1]
            [dirección reg.dds2_dato]
            [dato_l]
        """

        data = ['w', chr(reg), chr(addr1), chr(reg2), chr(dath), chr(reg), chr(addr2), chr(reg2), chr(datl)]
        response = self.usb.request(data, 4)
        logging.info(response)
        return response
    
    def _pulse_udclk(self):
        """ ['u']
            [dirección dds2_udclk]
            [0x00]
        """

        data = ['u', chr(self.dds_udclk), chr(0x00)]
        response = self.usb.request(data, 4)
        logging.info(response)
        return response
    
    def _read_code(self):
        """ ['g']
            [dirección del reg. de código]
        """

        data = ['g', chr(self.dds_code), chr(0x00)]
        response = self.usb.request(data, 4)
        logging.info(response)
        return response
    
    def _freq_parts(self, freq, n):
        """
        #fMCLK = 300Mhz o 200Mhz
        #valor = freq * base_freq / fMCLK
        """
        valor = freq * self.base_freq / self.fmlclk
        return bytes_reg_to_int_reg(bytes_to_reg(int_to_byte(valor), n))
    
    def load_frequency(self, freq, n):
        """
        :param freq: frecuencia a cargar 0 < freq <300000000
        :param n: 1 o 2
        :return:
        """
        # modo PC
        self._modo(0)
        print 0 <= freq <= 300000000
        # cargar registros de frecuencia
        freq_parts = self._freq_parts(freq, 6)
        freq_regs = {1: self.reg1, 2: self.reg2}.get(n, self.reg1)
        dd = zip(freq_parts, freq_regs)
        for f, r in dd:
            response = self._load(self.dds_reg, r, self.dds_data, f)
            logging.info("cargando dato")
            logging.info((r, f))
            logging.info("la operacion resulto")
            logging.info(str(response.value))

        # pulso udlck
        self._pulse_udclk()

        return

    def _phase_parts(self, phase, n):
        return bytes_reg_to_int_reg(bytes_to_reg(int_to_byte(phase), n))

    def load_phase(self, phase):
        """
          pasar a modo escritura de fases
          escribir fases
          pasar modo pc
        """
        print 0 <= phase <= 360
        # modo carga de fases
        self._modo(1)
        phase_parts = self._phase_parts(phase, 2)
        # escribir msb en 0x00 y lsb en 0x01
        self._load_phase(self.dds_cmd, 0x00, self.dds_ram, phase_parts[1], 0x01, phase_parts[1])
        # modo pc
        self._modo(0)
        return
