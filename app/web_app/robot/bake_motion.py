# -*- coding:utf-8 -*-

# Sample program
# Control of task(pro1.pcs) using b-cap

#b-cap Lib URL 
# https://github.com/DENSORobot/orin_bcap

from re import M
import web_app.pybcapclient.bcapclient as bcapclient
import datetime

class BakeMotion(object):

    def __init__(self):

### set IP Address , Port number and Timeout of connected RC8
        self.host = "192.168.0.1"
        self.port = 5007
        self.timeout = 2000

    def bake_crepe(self, all_cnt=None, gender :str=None, year=None, menu :str =None, count=None, order_time :str =None):
        ### set Parameter
        Name = ""
        Provider="CaoProv.DENSO.VRC"
        Machine = ("localhost")
        Option = ("")
       
        ### Connection processing of tcp communication
        m_bcapclient = bcapclient.BCAPClient(self.host,self.port,self.timeout)
        print("Open Connection")

        ### start b_cap Service
        m_bcapclient.service_start("")
        print("Send SERVICE_START packet")

        ### Connect to RC8 (RC8(VRC)provider)
        hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
        print("Connect RC8")

        if gender:
            SHandl_gender,IHandl_year, IHandl_count, SHandl_menu, SHandl_order_time = 0, 0, 0, 0, 0
            #Snum = 2*all_cnt-1  # all_cnt > 0
            Snum = 3*all_cnt-2 # all_cnt > 0
            Inum = 2*all_cnt+19
            SHandl_gender = m_bcapclient.controller_getvariable(hCtrl, "S" + str(Snum), "")
            IHandl_year = m_bcapclient.controller_getvariable(hCtrl, "I" + str(Inum), "")
            IHandl_count = m_bcapclient.controller_getvariable(hCtrl, "I" + str(Inum+1), "")
            SHandl_menu = m_bcapclient.controller_getvariable(hCtrl, "S" + str(Snum+1), "")
            SHandl_order_time = m_bcapclient.controller_getvariable(hCtrl, "S" + str(Snum+2), "")

            S_gender = gender
            I_year = year
            I_count = count
            S_menu = menu
            S_order_time = order_time

            serial = m_bcapclient.controller_execute(hCtrl, 'SysInfo', 0)
            print("Serial NO:{}".format(serial))
            state = m_bcapclient.controller_execute(hCtrl, 'SysState')
            print("SysState:{}".format(state)) # int

            m_bcapclient.variable_putvalue(SHandl_gender, S_gender) # write value of I*
            retS_gender = m_bcapclient.variable_getvalue(SHandl_gender) # read value of I*
            print("Read Variable S[{}] = {}".format(Snum, retS_gender))

            m_bcapclient.variable_putvalue(IHandl_year, I_year) # write value of I*
            retI_year = m_bcapclient.variable_getvalue(IHandl_year) # read value of I*
            print("Read Variable I[{}] = {}".format(Inum, retI_year))

            m_bcapclient.variable_putvalue(IHandl_count, I_count) # write value of I*
            retI_count = m_bcapclient.variable_getvalue(IHandl_count) # read value of I*
            print("Read Variable I[{}] = {}".format(Inum+1, retI_count))

            m_bcapclient.variable_putvalue(SHandl_menu, S_menu) # write value of I*
            retS_menu = m_bcapclient.variable_getvalue(SHandl_menu) # read value of I*
            print("Read Variable S[{}] = {}".format(Snum+1, retS_menu))

            m_bcapclient.variable_putvalue(SHandl_order_time, S_order_time) # write value of I*
            retS_order_time = m_bcapclient.variable_getvalue(SHandl_order_time) # read value of I*
            print("Read Variable S[{}] = {}".format(Snum+2, retS_order_time))

        else:
            pass

        ### get task(pro1) Object Handl
        HTask = 0
        HTask_name = "\Crepe_2022\Baking_2022"
        HTask = m_bcapclient.controller_gettask(hCtrl,HTask_name,"")

        #Start pro1
        #mode  1:One cycle execution, 2:Continuous execution, 3:Step forward
        mode = 1
        hr = m_bcapclient.task_start(HTask,mode,"")

        # Disconnect
        if(HTask != 0):
            m_bcapclient.task_release(HTask)
            print("Release " + HTask_name)
        #End If
        if(hCtrl != 0):
            m_bcapclient.controller_disconnect(hCtrl)
            print("Release Controller")
        #End If
        m_bcapclient.service_stop()
        print("B-CAP service Stop")
