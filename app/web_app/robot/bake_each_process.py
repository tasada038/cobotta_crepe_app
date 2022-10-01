# -*- coding:utf-8 -*-
# Send "Move" command to RC8
#b-cap Lib URL 
# https://github.com/DENSORobot/orin_bcap

import web_app.pybcapclient.bcapclient as bcapclient


class BakeEachProcess(object):
# DENSO ROBOT status
    def __init__(self):
        # set IP Address , Port number and Timeout of connected RC8
        self.host = "192.168.0.1"
        self.port = 5007
        self.timeout = 2000

        # set Parameter
        self.Name = ""
        self.Provider="CaoProv.DENSO.VRC"
        self.Machine = ("localhost")
        self.Option = ("")

        self.comp = 1
        self.loopflg = True
        self.ESC = 0x1B  # [ESC] virtual key code

    def start_bcap(self):
        # Connection processing of tcp communication
        self.m_bcapclient = bcapclient.BCAPClient(
            self.host,self.port,self.timeout
        )
        print("Open Connection")

        # start b_cap Service
        self.m_bcapclient.service_start("")
        print("Send SERVICE_START packet")

    def connect_rc8(self):
        # Connect to RC8 (RC8(VRC)provider)
        hCtrl = self.m_bcapclient.controller_connect(
            self.Name,self.Provider,self.Machine,self.Option
        )
        #print("Connect RC8")

        return hCtrl

    def control_robot(self):
        hCtrl = self.connect_rc8()
        HRobot = self.m_bcapclient.controller_getrobot(hCtrl,"Arm","")
        #print("AddRobot")

        self.m_bcapclient.robot_execute(HRobot,"TakeArm",[0,0])
        self.m_bcapclient.robot_execute(HRobot,"Motor",[1,0])
        self.m_bcapclient.robot_execute(HRobot,"ExtSpeed",100)

        return HRobot

    def release_bcap(self, hCtrl, HRobot):
        #End If
        if(hCtrl != 0):
            self.m_bcapclient.controller_disconnect(hCtrl)
        if(HRobot != 0):
            self.m_bcapclient.robot_release(HRobot)

    def stop_rc8(self):
        self.m_bcapclient.service_stop()
        print("B-CAP service Stop")

# Each Function
    def clear_error(self):
        hCtrl = self.connect_rc8()
        try:
            # Get Robot Handle
            hRobot = self.m_bcapclient.controller_getrobot(hCtrl, "Arm", "")
            hArm_Busy = self.m_bcapclient.robot_getvariable(hRobot, "@BUSY_STATUS")
            hE_Statu = self.m_bcapclient.controller_getvariable(hCtrl, "@EMERGENCY_STOP")
            # COBOTTA Version 2.8.0～
            # Comment out If version 2.7.X or lower
            #self.m_bcapclient.robot_execute(hRobot, "ManualResetPreparation", "")
            # COBOTTA Clear Error
            self.m_bcapclient.controller_execute(hCtrl, "ClearError")

            self.m_bcapclient.robot_execute(hRobot, "ManualResetPreparation", "")
            self.m_bcapclient.robot_execute(hRobot, "Motionpreparation")
            self.m_bcapclient.robot_execute(hRobot, "TakeArm")

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
                error_description = self.m_bcapclient.controller_execute(
                    hCtrl, "GetErrorDescription", errorcode_int)
                print("Error Description : " + error_description)
            else:
                print(e)

    def cobotta_gripper(self, Hand_name :str, arg1, arg2):
        hCtrl = self.connect_rc8()
        handmove_list = ["HandMoveA", "HandMoveH", "HandMoveR"]
        
        param = [arg1,arg2]
        ret = self.m_bcapclient.controller_execute(hCtrl,Hand_name,param)  

    def get_packingjnt(self):
        hCtrl = self.connect_rc8()
        HRobot = self.control_robot()

        # Ver.2.7.* ～
        packingjnt = self.m_bcapclient.robot_execute(HRobot,"GetPackingJoint")
        packing_pose = [packingjnt,"J","@P"]
        self.m_bcapclient.robot_move(HRobot,self.comp,packing_pose,"")

        self.release_bcap(hCtrl, HRobot)

# COBOTTA parameter
    def get_param(self):
        hCtrl = self.connect_rc8()
        HRobot = self.m_bcapclient.controller_getrobot(hCtrl,"Arm","")
        
        ### Get Position robot_execute 状態、値取得
        # CurJnt = J1,J2,J3,J4,J5,J6
        # CurPos = x,y,z,rx,ry,rz,fig
        curjnt = self.m_bcapclient.robot_execute(HRobot,"CurJnt")
        curpos = self.m_bcapclient.robot_execute(HRobot,"CurPos")
        #curfig = self.m_bcapclient.robot_execute(HRobot,"CurFig")
        torque = self.m_bcapclient.robot_execute(HRobot,"GetSrvData",4)
        speed = self.m_bcapclient.robot_execute(HRobot,"GetSrvData",17)

        return curjnt, curpos, torque, speed

    def get_p_data(self,p_data_num=1891,p_data_len=1):
        hCtrl = self.connect_rc8()
        HRobot = self.control_robot()
        variable_names = ['P*']
        variable_len_names = ['@VAR_P_LEN']
        ret_data = []
        for var_type, var_len  in zip(variable_names, variable_len_names):
            hvar_type = self.m_bcapclient.controller_getvariable(hCtrl, var_type)

            for id_num in range(p_data_num,p_data_num+p_data_len,1):
                self.m_bcapclient.variable_putid(hvar_type, id_num)
                ret_data.append(self.m_bcapclient.variable_getvalue(hvar_type))
            #print("ret_data:\n{}".format(ret_data))      

        return ret_data

    def get_f_data(self,f_data_num=0,f_data_len=1):
        self.start_bcap()
        hCtrl = self.connect_rc8()
        HRobot = self.control_robot()

        variable_names = ['F*']
        variable_len_names = ['@VAR_F_LEN']
        ret_data = []
        for var_type, var_len  in zip(variable_names, variable_len_names):
            hvar_type = self.m_bcapclient.controller_getvariable(hCtrl, var_type)
            for id_num in range(f_data_num,f_data_num+f_data_len,1):
                self.m_bcapclient.variable_putid(hvar_type, id_num)
                ret_data.append(self.m_bcapclient.variable_getvalue(hvar_type))
            print("ret_data:{}".format(ret_data))
            break

        self.stop_rc8()

        return ret_data

    def write_d_param(self, d_num, add_value):
        self.start_bcap()
        hCtrl = self.connect_rc8()

        DHandl, newval = 0.0, 0.0
        DHandl = self.m_bcapclient.controller_getvariable(hCtrl, "D" + str(d_num), "")
    
        # read value of *
        retd = self.m_bcapclient.variable_getvalue(DHandl)
        print("Read Variable D[{}] = {}".format(d_num, retd))

        # add value
        float_add_value = float(add_value)
        newval = retd + float_add_value
        print("new_val:{}".format(newval))

        # write value of *
        self.m_bcapclient.variable_putvalue(DHandl, newval)
        print("Write Variable :newval = %d" % newval)
        # read value of *
        retd = self.m_bcapclient.variable_getvalue(DHandl)
        print("Read Variable D[{}] = {}".format(d_num, retd))
        # End for

        self.stop_rc8()

        return retd

    def read_d_param(self, d_num):
        self.start_bcap()
        hCtrl = self.connect_rc8()

        DHandl, newval = 0.0, 0.0
        DHandl = self.m_bcapclient.controller_getvariable(hCtrl, "D" + str(d_num), "")
    
        # read value of *
        retd = self.m_bcapclient.variable_getvalue(DHandl)
        print("Read Variable D[{}] = {}".format(d_num, retd))

        self.stop_rc8()

        return retd

# COBOTTA Motion
    def task_motion(self, HTask_name :str):
        hCtrl = self.connect_rc8()
        HTask = self.m_bcapclient.controller_gettask(hCtrl,HTask_name,"")
        HTaskState = self.m_bcapclient.task_getvariable(
            HTask,"@STATUS_DETAILS",""
        )
        _ = self.m_bcapclient.task_start(HTask,self.comp,"")
        print("task_motion:{}".format(HTask_name))

        while self.loopflg:
            TaskStatus = self.m_bcapclient.variable_getvalue(HTaskState)
            #print("TaskStatus : ",TaskStatus)
            if(TaskStatus == 2):
                self.loopflg=False

        self.loopflg=True

    def move_motion(self, position :str):
        hCtrl = self.connect_rc8()
        HRobot = self.control_robot()
        self.m_bcapclient.robot_move(HRobot,self.comp,position,"")
        print("Complete Move P," + position)
        #self.m_bcapclient.robot_execute(HRobot,"Arrive",100)
        self.release_bcap(hCtrl, HRobot)

    def move_position(self,HRobot,position_value, trajectory :str):
        #hCtrl = self.connect_rc8()
        #HRobot = self.control_robot()

        Pose = [position_value,trajectory,"@P"]
        self.m_bcapclient.robot_move(HRobot,self.comp,Pose,"")
        #self.release_bcap(hCtrl, HRobot)

    def move_xyz(self,x,y,z,rx=180,ry=0,rz=-180,fig=261):
        hCtrl = self.connect_rc8()
        HRobot = self.control_robot()

        position_Value = [x,y,z,rx,ry,rz,fig]
        Pose = [position_Value,"P","@P"]
        self.m_bcapclient.robot_move(HRobot,self.comp,Pose,"")
        print("Move xyz:P({0},{1},{2},{3},{4},{5},{6})"\
              .format(x,y,z,rx,ry,rz,fig))

        self.release_bcap(hCtrl, HRobot)

# Error Recovery
    def move_error_recovery_xyz(
        self,rec_x=0,rec_y=0,rec_z=0,\
        rec_rx=0, rec_ry=0, rec_rz=0
        ):

        hCtrl = self.connect_rc8()
        HRobot = self.control_robot()

        x_value, y_value, z_value = rec_x, rec_y, rec_z
        rx_value, ry_value, rz_value = rec_rx, rec_ry, rec_rz
        _,curpos_value,_,_ = self.get_param()
        curpos_value[0] += x_value
        curpos_value[1] += y_value
        curpos_value[2] += z_value
        curpos_value[3] += rx_value
        curpos_value[4] += ry_value
        curpos_value[5] += rz_value
        next_pose = [curpos_value,"P","@P"]
        self.m_bcapclient.robot_move(HRobot,self.comp,next_pose,"")

        self.release_bcap(hCtrl, HRobot)

    def move_error_recovery_jnt(
        self,j1=0,j2=0,j3=0,\
        j4=0, j5=0, j6=0
        ):

        hCtrl = self.connect_rc8()
        HRobot = self.control_robot()

        j1_value,j2_value,j3_value = j1,j2,j3
        j4_value,j5_value,j6_value = j4,j5,j6

        curjnt_value,_,_,_ = self.get_param()
        curjnt_value[0] += j1_value
        curjnt_value[1] += j2_value
        curjnt_value[2] += j3_value
        curjnt_value[3] += j4_value
        curjnt_value[4] += j5_value
        curjnt_value[5] += j6_value
        next_pose = [curjnt_value,"J","@P"]
        self.m_bcapclient.robot_move(HRobot,self.comp,next_pose,"")

        self.release_bcap(hCtrl, HRobot)

# Bake Each Process
# Initial Pos
    def bake_initial(self):
        self.start_bcap()  # start B_CAP service
        self.move_motion("@P P2056")
        self.stop_rc8()

# HandOpen
    def bake_hand_open(self):
        self.start_bcap()  # start B_CAP service
        self.cobotta_gripper("HandMoveA", 30, 100)
        self.stop_rc8()  
# Packing
    def bake_packing(self):
        self.start_bcap()  # start B_CAP service
        self.get_packingjnt()
        self.stop_rc8() 

# Bake Process
    def bake_oiling(self):
        self.start_bcap()  # start B_CAP service
        self.task_motion("Crepe_2022/oiling")
        self.stop_rc8()

    def bake_redol(self):
        self.start_bcap()  # start B_CAP service
        self.task_motion("Crepe_2022/redol")
        self.stop_rc8()

    def bake_tonnbo(self):
        self.start_bcap()  # start B_CAP service
        self.task_motion("Crepe_2022/tonnbo")
        self.stop_rc8()

    def bake_tonnbo4_variable(self,tonnbo_z):
        p_data_num = 2040
        p_data_len = 10
        self.start_bcap()  # start B_CAP service
        tonnbo_variable = self.get_p_data(p_data_num,p_data_len)
        for i in range(p_data_len):
            tonnbo_variable[i][2] += tonnbo_z
        print("ret_data:\n{}".format(tonnbo_variable))
        self.stop_rc8()

        self.start_bcap()
        hCtrl = self.connect_rc8()
        HRobot = self.control_robot()
        for i in range(p_data_len):
            self.move_position(HRobot,tonnbo_variable[i],'L')
        self.release_bcap(hCtrl, HRobot)
        self.stop_rc8()  

    def bake_hera(self):
        self.start_bcap()  # start B_CAP service
        self.task_motion("Crepe_2022/hera_long")
        self.stop_rc8()
    

# Recovery XYZ
    def bake_recovery_addx(self):
        self.start_bcap()  # start B_CAP service
        #self.cobotta_gripper("HandMoveH", 20, True)
        self.cobotta_gripper("HandMoveA", 30, 100)
        self.move_error_recovery_xyz(20,0,0,0,0,0)
        self.stop_rc8()

    def bake_recovery_subx(self):
        self.start_bcap()  # start B_CAP service

        self.cobotta_gripper("HandMoveA", 30, 100)
        self.move_error_recovery_xyz(-20,0,0,0,0,0)
        self.stop_rc8()

    def bake_recovery_addy(self):
        self.start_bcap()  # start B_CAP service

        self.cobotta_gripper("HandMoveA", 30, 100)
        self.move_error_recovery_xyz(0,20,0,0,0,0)
        self.stop_rc8()

    def bake_recovery_suby(self):
        self.start_bcap()  # start B_CAP service
        self.cobotta_gripper("HandMoveA", 30, 100)
        self.move_error_recovery_xyz(0,-20,0,0,0,0)
        self.stop_rc8()

    def bake_recovery_addz(self):
        self.start_bcap()  # start B_CAP service
        self.cobotta_gripper("HandMoveA", 30, 100)
        self.move_error_recovery_xyz(0,0,20,0,0,0)
        self.stop_rc8()

    def bake_recovery_subz(self):
        self.start_bcap()  # start B_CAP service
        self.cobotta_gripper("HandMoveA", 30, 100)
        self.move_error_recovery_xyz(0,0,-20,0,0,0)
        self.stop_rc8()

# Recovery Jnt
    def bake_recovery_addj1(self):
        self.start_bcap()  # start B_CAP service
        #self.cobotta_gripper("HandMoveH", 20, True)
        self.cobotta_gripper("HandMoveA", 30, 100)
        self.move_error_recovery_jnt(20,0,0,0,0,0)
        self.stop_rc8()

    def bake_recovery_subj1(self):
        self.start_bcap()  # start B_CAP service
        #self.cobotta_gripper("HandMoveH", 20, True)
        self.cobotta_gripper("HandMoveA", 30, 100)
        self.move_error_recovery_jnt(-20,0,0,0,0,0)
        self.stop_rc8()

    def bake_recovery_addj2(self):
        self.start_bcap()  # start B_CAP service
        #self.cobotta_gripper("HandMoveH", 20, True)
        self.cobotta_gripper("HandMoveA", 30, 100)
        self.move_error_recovery_jnt(0,20,0,0,0,0)
        self.stop_rc8()

    def bake_recovery_subj2(self):
        self.start_bcap()  # start B_CAP service
        #self.cobotta_gripper("HandMoveH", 20, True)
        self.cobotta_gripper("HandMoveA", 30, 100)
        self.move_error_recovery_jnt(0,-20,0,0,0,0)
        self.stop_rc8()       


if __name__ == '__main__':
    robot = BakeEachProcess()
    robot.bake_tonnbo4_variable(3)
    