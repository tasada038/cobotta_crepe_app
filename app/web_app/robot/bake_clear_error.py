import random
import time

import web_app.pybcapclient.bcapclient as bcapclient


class BakeClearError(object):

    def __init__(self):
        # set IP Address , Port number and Timeout of connected RC8
        self.host = "192.168.0.1"
        self.port = 5007
        self.timeout = 2000

    def bake_clear_error(self):
        # Connection processing of tcp communication
        m_bcapclient = bcapclient.BCAPClient(self.host, self.port, self.timeout)
        print("Open Connection")

        # start b_cap Service
        m_bcapclient.service_start("")
        print("Send SERVICE_START packet")

        # set Parameter
        Name = ""
        Provider = "CaoProv.DENSO.VRC"
        Machine = "localhost"
        Option = ""

        try:
            # Connect to RC8 (RC8(VRC)provider) , Get Controller Handle
            hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
            print("Connect RC8")
            # Get Robot Handle
            hRobot = m_bcapclient.controller_getrobot(hCtrl, "Arm", "")
            hArm_Busy = m_bcapclient.robot_getvariable(hRobot, "@BUSY_STATUS")
            hE_Statu = m_bcapclient.controller_getvariable(hCtrl, "@EMERGENCY_STOP")
            # COBOTTA Version 2.8.0～
            # Comment out If version 2.7.X or lower
            #m_bcapclient.robot_execute(hRobot, "ManualResetPreparation", "")
            # COBOTTA Clear Error
            m_bcapclient.controller_execute(hCtrl, "ClearError")

            #m_bcapclient.robot_execute(hRobot, "ManualResetPreparation", "")
            m_bcapclient.robot_execute(hRobot, "Motionpreparation")
            m_bcapclient.robot_execute(hRobot, "TakeArm")

        except Exception as e:
            print('=== ERROR Description ===')
            if str(type(e)) == "<class 'web_app.pybcapclient.orinexception.ORiNException'>":
                print(e)
                errorcode_int = int(str(e))
                if errorcode_int < 0:
                    errorcode_hex = format(errorcode_int & 0xffffffff, 'x')
                else:
                    errorcode_hex = hex(errorcode_int)
                print("Error Code : 0x" + str(errorcode_hex))
                error_description = m_bcapclient.controller_execute(
                    hCtrl, "GetErrorDescription", errorcode_int)
                print("Error Description : " + error_description)
            else:
                print(e)

        finally:
            m_bcapclient.robot_execute(hRobot, "GiveArm")
            # DisConnect
            if(hRobot != 0):
                m_bcapclient.robot_release(hRobot)
                print("Release Robot Handle")
            # End If
            if(hCtrl != 0):
                m_bcapclient.controller_disconnect(hCtrl)
                print("Release Controller")
            # End If
            m_bcapclient.service_stop()
            print("B-CAP service Stop")


if __name__ == '__main__':
    robot = BakeClearError()
    robot.bake_clear_error()