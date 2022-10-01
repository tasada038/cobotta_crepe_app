from multiprocessing import Process, Pool
from web_app.robot.bake_motion import BakeMotion
from web_app.robot.topping_motion import ToppingMotion

import time

class MultiMotion(object):

    def __init__(self):
        self.robot_1 = BakeMotion()
        self.robot_2 = ToppingMotion()

        self.delay_time = 87+14

    def bake_cobotta(self):
        self.robot_1.bake_crepe()

    def topping_cobotta(self,menu_data):
        self.robot_2.topping_crepe(menu_data)

    def multi_process(self,menu_data, all_cnt, gender, year, menu, count, order_time):
        self.robot_1.bake_crepe(all_cnt, gender, year, menu, count, order_time)

        # Delay Until the bakeing COBOTTA is finished
        time.sleep(self.delay_time)
        self.robot_2.topping_crepe(menu_data)

    # menu
    def multi_whip_strawberry_choco(self, all_cnt, gender, year, menu, count, order_time):
        self.robot_1.bake_crepe(all_cnt, gender, year, menu, count, order_time)
        time.sleep(self.delay_time)
        self.robot_2.topping_whip_strawberry_choco()

    def multi_whip_caramel_flake(self, all_cnt, gender, year, menu, count, order_time):
        self.robot_1.bake_crepe(all_cnt, gender, year, menu, count, order_time)
        time.sleep(self.delay_time)
        self.robot_2.topping_whip_caramel_flake()

    def multi_whip_choco_almond(self, all_cnt, gender, year, menu, count, order_time):
        self.robot_1.bake_crepe(all_cnt, gender, year, menu, count, order_time)
        time.sleep(self.delay_time)
        self.robot_2.topping_whip_choco_almond()

    def multi_whip_choco_banana(self):
        self.robot_1.bake_crepe()
        time.sleep(self.delay_time)
        self.robot_2.topping_whip_choco_banana()

    def multi_custard_strawberry_biscuits(self):
        self.robot_1.bake_crepe()
        time.sleep(self.delay_time)
        self.robot_2.topping_custard_strawberry_biscuits()

if __name__ == '__main__':
    p1 = Process(target=MultiMotion.bake_cobotta)
    p2 = Process(target=MultiMotion.topping_cobotta)
    p1.start()
    p2.start()
