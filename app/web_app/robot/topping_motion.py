# -*- coding:utf-8 -*-

# Sample program
# Control of task(pro1.pcs) using b-cap

#b-cap Lib URL 
# https://github.com/DENSORobot/orin_bcap

import web_app.pybcapclient.bcapclient as bcapclient
import time

class ToppingMotion(object):

    def __init__(self):
        self.host = "192.168.0.2"
        self.port = 5007
        self.timeout = 2000

    def crepe_serve_version(self, menu_data):
        # Custard_Menu
        HTask_name = ""
        if ("Custard" in menu_data):
            if ("Chocolate" in menu_data):
                if ("Chocotip" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Choco_chocolate"
                elif ("Cocoa" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Choco_biscuits"
                elif ("Corn" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Choco_flake"
                elif ("Almond" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Choco_almond"
                elif ("Banana" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Choco_drybanana"
                elif ("Fruit" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Choco_fruit"                
            elif ("Strawberry" in menu_data):
                if ("Chocotip" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Strawberry_chocolate"
                elif ("Cocoa" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Strawberry_biscuits"
                elif ("Corn" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Strawberry_flake"
                elif ("Almond" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Strawberry_almond"
                elif ("Banana" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Strawberry_drybanana"
                elif ("Fruit" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Strawberry_fruit"                
            elif ("Blueberry" in menu_data):
                if ("Chocotip" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Blueberry_chocolate"
                elif ("Cocoa" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Blueberry_biscuits"
                elif ("Corn" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Blueberry_flake"
                elif ("Almond" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Blueberry_almond"
                elif ("Banana" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Blueberry_drybanana"
                elif ("Fruit" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Blueberry_fruit"                
            elif ("Caramel" in menu_data):
                if ("Chocotip" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Caramel_chocolate"
                elif ("Cocoa" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Caramel_biscuits"
                elif ("Corn" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Caramel_flake"
                elif ("Almond" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Caramel_almond"
                elif ("Banana" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Caramel_drybanana"
                elif ("Fruit" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Caramel_fruit"                
            elif ("Matcha" in menu_data):
                if ("Chocotip" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Matcha_chocolate"
                elif ("Cocoa" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Matcha_biscuits"
                elif ("Corn" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Matcha_flake"
                elif ("Almond" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Matcha_almond"
                elif ("Banana" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Matcha_drybanana"
                elif ("Fruit" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Matcha_fruit"                
            elif ("Honey" in menu_data):
                if ("Chocotip" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Honey_chocolate"
                elif ("Cocoa" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Honey_biscuits"
                elif ("Corn" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Honey_flake"
                elif ("Almond" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Honey_almond"
                elif ("Banana" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Honey_drybanana"
                elif ("Fruit" in menu_data):
                    HTask_name = "\Menu_Custard_ver\Custard_Honey_fruit"                
            else:
                # Random
                HTask_name = "\Menu_Custard_ver\Custard_Choco_biscuits"
            
        # Whip_Menu
        if ("Whip" in menu_data):
            if ("Chocolate" in menu_data):
                if ("Chocotip" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Choco_chocolate"
                elif ("Cocoa" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Choco_biscuits"
                elif ("Corn" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Choco_flake"
                elif ("Almond" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Choco_almond"
                elif ("Banana" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Choco_drybanana"
                elif ("Fruit" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Choco_fruit" 
            elif ("Strawberry" in menu_data):
                if ("Chocotip" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Strawberry_chocolate"
                elif ("Cocoa" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Strawberry_biscuits"
                elif ("Corn" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Strawberry_flake"
                elif ("Almond" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Strawberry_almond"
                elif ("Banana" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Strawberry_drybanana"
                elif ("Fruit" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Strawberry_fruit"
            elif ("Blueberry" in menu_data):
                if ("Chocotip" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Blueberry_chocolate"
                elif ("Cocoa" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Blueberry_biscuits"
                elif ("Corn" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Blueberry_flake"
                elif ("Almond" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Blueberry_almond"
                elif ("Banana" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Blueberry_drybanana"
                elif ("Fruit" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Blueberry_fruit" 
            elif ("Caramel" in menu_data):
                if ("Chocotip" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Caramel_chocolate"
                elif ("Cocoa" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Caramel_biscuits"
                elif ("Corn" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Caramel_flake"
                elif ("Almond" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Caramel_almond"
                elif ("Banana" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Caramel_drybanana"
                elif ("Fruit" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Caramel_fruit" 
            elif ("Matcha" in menu_data):
                if ("Chocotip" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Matcha_chocolate"
                elif ("Cocoa" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Matcha_biscuits"
                elif ("Corn" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Matcha_flake"
                elif ("Almond" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Matcha_almond"
                elif ("Banana" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Matcha_drybanana"
                elif ("Fruit" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Matcha_fruit"                
            elif ("Honey" in menu_data):
                if ("Chocotip" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Honey_chocolate"
                elif ("Cocoa" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Honey_biscuits"
                elif ("Corn" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Honey_flake"
                elif ("Almond" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Honey_almond"
                elif ("Banana" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Honey_drybanana"
                elif ("Fruit" in menu_data):
                    HTask_name = "\Menu_Whip_ver\Whip_Honey_fruit"   
            else:
                # Random
                HTask_name = "\Menu_Whip_ver\Whip_Strawberry_flake"

            """
             # Topping List
            topping_list = ["Chocotip", "Cocoa", "Corn", \
                            "Almond", "Banana", "Marron"]

            # Source List
            source_list = ["Chocolate", "Caramel, "Strawberry", \
                           "Blueberry", "Matcha, "Honey"]
            """

        return HTask_name

    def topping_crepe(self,menu_data):
            ### Connection processing of tcp communication
            m_bcapclient = bcapclient.BCAPClient(self.host,self.port,self.timeout)
            print("Open Connection")

            ### start b_cap Service
            m_bcapclient.service_start("")
            print("Send SERVICE_START packet")

            ### set Parameter
            Name = ""
            Provider="CaoProv.DENSO.VRC"
            Machine = ("localhost")
            Option = ("")

            ### Connect to RC8 (RC8(VRC)provider)
            hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
            print("Connect RC8")
            ### get task(pro1) Object Handl
            HTask = 0

            HTask_name = self.crepe_serve_version(menu_data)

            HTask = m_bcapclient.controller_gettask(hCtrl,HTask_name,"")
            hr = m_bcapclient.task_start(HTask,1,"")

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

    def topping_whip_strawberry_choco(self):
        m_bcapclient = bcapclient.BCAPClient(self.host,self.port,self.timeout)
        m_bcapclient.service_start("")
        Name = ""
        Provider="CaoProv.DENSO.VRC"
        Machine = ("localhost")
        Option = ("")

        hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
        HTask = 0
        HTask_name = "\Menu_Whip_ver\Whip_Strawberry_chocolate"
        HTask = m_bcapclient.controller_gettask(hCtrl,HTask_name,"")
        mode = 1
        hr = m_bcapclient.task_start(HTask,mode,"")

        if(HTask != 0):
            m_bcapclient.task_release(HTask)
        if(hCtrl != 0):
            m_bcapclient.controller_disconnect(hCtrl)
        m_bcapclient.service_stop()

    def topping_whip_caramel_flake(self):
        m_bcapclient = bcapclient.BCAPClient(self.host,self.port,self.timeout)
        m_bcapclient.service_start("")
        Name = ""
        Provider="CaoProv.DENSO.VRC"
        Machine = ("localhost")
        Option = ("")

        hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
        HTask = 0
        HTask_name = "\Menu_Whip_ver\Whip_Caramel_flake"
        HTask = m_bcapclient.controller_gettask(hCtrl,HTask_name,"")
        mode = 1
        hr = m_bcapclient.task_start(HTask,mode,"")

        if(HTask != 0):
            m_bcapclient.task_release(HTask)
        if(hCtrl != 0):
            m_bcapclient.controller_disconnect(hCtrl)
        m_bcapclient.service_stop()

    def topping_whip_choco_almond(self):
        m_bcapclient = bcapclient.BCAPClient(self.host,self.port,self.timeout)
        m_bcapclient.service_start("")
        Name = ""
        Provider="CaoProv.DENSO.VRC"
        Machine = ("localhost")
        Option = ("")

        hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
        HTask = 0
        HTask_name = "\Menu_Whip_ver\Whip_Choco_almond"
        HTask = m_bcapclient.controller_gettask(hCtrl,HTask_name,"")
        mode = 1
        hr = m_bcapclient.task_start(HTask,mode,"")

        if(HTask != 0):
            m_bcapclient.task_release(HTask)
        if(hCtrl != 0):
            m_bcapclient.controller_disconnect(hCtrl)
        m_bcapclient.service_stop()

    def topping_whip_choco_banana(self):
        m_bcapclient = bcapclient.BCAPClient(self.host,self.port,self.timeout)
        m_bcapclient.service_start("")
        Name = ""
        Provider="CaoProv.DENSO.VRC"
        Machine = ("localhost")
        Option = ("")

        hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
        HTask = 0
        HTask_name = "\Menu_Whip_ver\Whip_Choco_drybanana"
        HTask = m_bcapclient.controller_gettask(hCtrl,HTask_name,"")
        mode = 1
        hr = m_bcapclient.task_start(HTask,mode,"")

        if(HTask != 0):
            m_bcapclient.task_release(HTask)
        if(hCtrl != 0):
            m_bcapclient.controller_disconnect(hCtrl)
        m_bcapclient.service_stop()

    def topping_custard_strawberry_biscuits(self):
        m_bcapclient = bcapclient.BCAPClient(self.host,self.port,self.timeout)
        m_bcapclient.service_start("")
        Name = ""
        Provider="CaoProv.DENSO.VRC"
        Machine = ("localhost")
        Option = ("")

        hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
        HTask = 0
        HTask_name = "\Menu_Custard_ver\Custard_Strawberry_biscuits"
        HTask = m_bcapclient.controller_gettask(hCtrl,HTask_name,"")
        mode = 1
        hr = m_bcapclient.task_start(HTask,mode,"")

        if(HTask != 0):
            m_bcapclient.task_release(HTask)
        if(hCtrl != 0):
            m_bcapclient.controller_disconnect(hCtrl)
        m_bcapclient.service_stop()