# -*- coding: utf-8 -*-
import logging


class LangProg:

    cod_continue = 0x01
    cod_lazo = 0x02
    cod_retl = 0x03
    cod_fin = 0x07
    pat_

    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG,
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        return

    def _continue(self, patron, demora):
        return