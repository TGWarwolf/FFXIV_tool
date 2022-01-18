from tkinter import Tk, Label, Button, Canvas, Radiobutton
from tkinter import W,E,N,S
import math
import sys
import os

BAIQIU=0
HONGQIU=1
LVQIU=2
LANQIU=3
DAJINZHAN=4
CHANGCHIXU=5
BALL_STATUS=[(BAIQIU, "白球", "white"), (HONGQIU, "红球", "red"), (LVQIU, "高效", "green"), (LANQIU, "结实", "blue"), (DAJINZHAN, "大进展", "mediumblue"), (CHANGCHIXU, "长持续", "purple")]

START = 0
PRO_FIN = 1
WORK_FIN = 2
FINISH = 3
#工匠属性及配方属性
class Configuration:
    def __init__(self, Craftsmanship, Control, CP, Progress, Quality, Durability):
        #作业精度 Craftsmanship
        self.Craftsmanship = Craftsmanship
        #加工精度 Control
        self.Control = Control
        #制作力 CP
        self.CP = CP
        #作业进度 Progress
        self.Progress = Progress
        #品质 Quality
        self.Quality = Quality
        #耐久 Durability
        self.Durability = Durability

#进行中的状态：
class Status:
    def __init__(self,Step=1):
        #工次 step
        self.Step=Step


class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("四期高难人力轮椅  by Tg狼人@银泪湖")
        
        self.window_width=300
        
        self.Status = Status(Step=1)
        
        self.Stage = START
        self.work_eff = 0
        self.work_eff_all = 2570
        
        self.Config = Configuration(Craftsmanship=2758, Control=2901, CP=651, Progress=12046, Quality=81447, Durability=55)
        
        self.now_CP = self.Config.CP
        self.work = 0.8* (0.21 * self.Config.Craftsmanship + 2) * (10000 + self.Config.Craftsmanship) / (10000 + 2620)
        
        self.pro = 0.6 * (0.35 * self.Config.Control + 35) * (10000 + self.Config.Control) / (10000 + 2540)
       
        
        self.work_now = 0
        self.pro_now = 0
        self.Durability_now = 55
        
        self.Neijing = 0
        self.Zhangwo = 0
        self.Jianyue = 0
        self.Chongjing=0
        self.Gaige = 0
        self.Guancha = 0
        self.Kuobu = 0
        
        self.ball = BAIQIU
        self.ball_button = []
        for status,btext,color in BALL_STATUS:
            self.ball_button += [Radiobutton(master, variable=self.ball, value=status, text = btext, bg=color, activebackground=color, indicatoron=False, command=lambda s=status:self.ball_change(s))]
            self.ball_button[status].grid(row=5, column=status)
        self.ball_button[BAIQIU].select()
        self.recommend_label = Label(master, text="推荐技能：闲静")

        self.buff_label = Label(master, text="四期高难模拟器  by Tg狼人@银泪湖")
        self.canvas_label = Label(master, text="进展\n品质\n耐久\nCP")
        self.canvas = Canvas(master, bg='white', height=80, width=self.window_width)
        
        self.work_rec = self.canvas.create_rectangle(0, 0, self.work_now/self.Config.Progress*self.window_width, 19, width=0, fill='green')
        self.pro_rec = self.canvas.create_rectangle(0, 20, self.pro_now/self.Config.Quality*self.window_width, 39, width=0, fill='red')
        self.Durability_rec = self.canvas.create_rectangle(0, 40, self.Durability_now/self.Config.Durability*self.window_width, 59, width=0, fill='purple')
        self.CP_rec = self.canvas.create_rectangle(0, 60, self.now_CP/self.Config.CP*self.window_width, 80, width=0, fill='green')
        
        
        self.canvas_data = Label(master, text= self.getDataText())
        
        self.xianjing_button = Button(master, text="闲静", command= self.xianjing)
        self.chongjing_button = Button(master, text="崇敬", command= self.chongjingj)
        self.gaige_button = Button(master, text="改革", command= self.gaigej)
        self.zhangwo_button = Button(master, text="掌握", command=self.zhangwoj)
        self.changqijianyue_button = Button(master, text="长期俭约", command=self.changqijianyue)
        self.kuobu_button = Button(master, text="阔步", command=self.kuobuj)
        self.guancha_button = Button(master, text="观察", command=self.guanchaj)
        
        self.gaosuzhizuo_button = Button(master, text="高速制作", command=self.gaosuzhizuo)
        self.mofanzhizuo_button = Button(master, text="模范制作", command=self.mofanzhizuo)
        self.jizhongzhizuo_button = Button(master, text="集中制作", command=self.jizhongzhizuo)
        self.zhushizhizuo_button = Button(master, text="注视制作", command=self.zhushizhizuo)
        self.zhizuo_button = Button(master, text="制作", command=self.zhizuo)
        
        self.mijue_button = Button(master, text="秘诀", command=self.mijue)
        self.jingxiu_button = Button(master, text="精修", command=self.jingxiu)
        
        self.shibai_button = Button(master, text="失败10耐", command=self.shibai)
        
        
        self.cangcu_button = Button(master, text="仓促", command=self.cangcu)
        self.piliaojiagong_button = Button(master, text="坯料加工", command=self.piliaojiagong)
        self.jizhongjiagong_button = Button(master, text="集中加工", command=self.jizhongjiagong)
        self.zhushijiagong_button = Button(master, text="注视加工", command=self.zhushijiagong)
        self.jianyuejiagong_button = Button(master, text="俭约加工", command=self.jianyuejiagong)
        self.bierge_button = Button(master, text="比尔格", command=self.bierge)

        self.close_button = Button(master, text="Close", command=master.quit)
        self.reset_button = Button(master, text="重来", command=self.restart_program)
        
        self.buff_label.grid(row= 0, columnspan=10, sticky=W)
        
        self.canvas_label.grid(row=1,column=0)
        self.canvas_data.grid(row=1, column=1)
        self.canvas.grid(row=1, column=2, columnspan=10)
        
        self.xianjing_button.grid(row=2, column=0)
        self.chongjing_button.grid(row=2, column=1)
        self.gaige_button.grid(row=2, column=2)
        self.zhangwo_button.grid(row=2, column=3)
        self.changqijianyue_button.grid(row=2, column=4)
        self.kuobu_button.grid(row=2, column=5)
        self.guancha_button.grid(row=2, column=6)
        
        self.gaosuzhizuo_button.grid(row=3, column=0)
        self.mofanzhizuo_button.grid(row=3, column=1)
        self.jizhongzhizuo_button.grid(row=3, column=2)
        self.zhushizhizuo_button.grid(row=3,column=3)
        self.zhizuo_button.grid(row=3, column=4)
        self.mijue_button.grid(row=3, column=5)
        self.jingxiu_button.grid(row=3, column=6)
        
        
        self.cangcu_button.grid(row=4, column=0)
        self.piliaojiagong_button.grid(row=4, column=1)
        self.jizhongjiagong_button.grid(row=4, column=2)
        self.zhushijiagong_button.grid(row=4,column=3)
        self.jianyuejiagong_button.grid(row=4, column=4)
        self.bierge_button.grid(row=4, column=5)
        
        self.shibai_button.grid(row=4, column=6)
        
        self.close_button.grid(row=6, column=0)
        self.reset_button.grid(row=6, column=1)
        self.recommend_label.grid(row=6, column=2, columnspan=10)
        
        
    def ball_change(self, status):
        self.ball = status
        self.update_recommend()
        
        
    def xianjing(self):
        if self.Status.Step>1:
            print("闲静错误：只能在第一回合使用")
            return
        print("闲静")
        self.exe(0, 100, 10, 24)
        self.Neijing = 3
        self.update_status()
    
    def chongjingj(self):
        if_changchixu = 0
        if self.ball == CHANGCHIXU:
            if_changchixu = 1
        if 0==self.exe(0, 0, 0, 18):
            return
        print("崇敬")
        self.Chongjing = 5 + 2 * if_changchixu
        self.update_status()
    
    def gaigej(self):
        if_changchixu = 0
        if self.ball == CHANGCHIXU:
            if_changchixu = 1
        if self.exe(0, 0, 0, 18)==0:
            return
        print("改革")
        self.Gaige = 5 + 2 * if_changchixu
        self.update_status()
        
    def changqijianyue(self):
        if_changchixu = 0
        if self.ball == CHANGCHIXU:
            if_changchixu = 1
        if self.exe(0, 0, 0, 98)==0:
            return
        print("长期俭约")
        self.Jianyue = 9 + 2 * if_changchixu
        self.update_status()
    
    def zhangwoj(self):
        if_changchixu = 0
        if self.ball == CHANGCHIXU:
            if_changchixu = 1
        if self.exe(0, 0, 0, 96)==0:
            return
        print("掌握")
        self.Zhangwo = 9 + 2 * if_changchixu
        self.Durability_now-= 5
        self.update_status()
    
    def kuobuj(self):
        if_changchixu = 0
        if self.ball == CHANGCHIXU:
            if_changchixu = 1
        if self.exe(0, 0, 0, 32)==0:
            return
        print("阔步")
        self.Kuobu = 4 + 2 * if_changchixu
        self.update_status()
    
    def guanchaj(self):
        if self.exe(0, 0, 0, 7)==0:
            return
        print("观察")
        self.Guancha = 2
        self.update_status()
    def zhizuo(self):
        print("制作")
        self.exe(120, 0, 10, 0)
        self.update_status()
        
    def mofanzhizuo(self):
        if self.exe(150, 0, 10, 7)==0:
            return
        print("模范制作")
        self.update_status()
        
    def jizhongzhizuo(self):
        if self.ball != HONGQIU:
            print("不是红球！")
            return
        if self.exe(400, 0, 10, 6)==0:
            return
        print("集中制作")
        self.update_status()
        
    def zhushizhizuo(self):
        if self.exe(200, 0, 10, 5)==0:
            return
        print("注视制作")
        self.update_status()
    
    def gaosuzhizuo(self):
        print("高速制作")
        self.exe(500, 0, 10, 0)
        self.update_status()
        
    def mijue(self):
        if self.ball != HONGQIU:
            print("不是红球！")
            return
        self.exe(0,0,0,-20)
        print("秘诀")
        self.update_status()
        
    def jingxiu(self):
        if self.exe(0, 0, -30, 88)==0:
            return
        print("精修")
        self.update_status()
        
    def cangcu(self):
        print("仓促")
        self.exe(0, 100, 10, 0)
        if self.Neijing>0:
            self.Neijing = min(self.Neijing+1, 11)
        self.update_status()
    
    def piliaojiagong(self):
        if self.exe(0, 200, 20, 40)==0:
            return
        print("坯料加工")
        if self.Neijing>0:
            self.Neijing = min(self.Neijing+2, 11)
        self.update_status()
    
    def jizhongjiagong(self):
        if self.ball != HONGQIU:
            print("不是红球！")
            return
        if self.exe(0, 150, 10, 18)==0:
            return
        print("集中加工")
        if self.Neijing>0:
            self.Neijing = min(self.Neijing+2, 11)
        self.update_status()
        
    def zhushijiagong(self):
        if self.exe(0, 150, 10, 18)==0:
            return
        print("注视加工")
        if self.Neijing>0:
            self.Neijing = min(self.Neijing+1, 11)
        self.update_status()
    
    def jianyuejiagong(self):
        if self.Jianyue > 0:
            print("俭约加工不能使用！")
            return
        if self.exe(0, 100, 5, 25)==0:
            return
        print("俭约加工")
        if self.Neijing>0:
            self.Neijing = min(self.Neijing+1, 11)
        self.update_status()
    
    def bierge(self):
        if self.Neijing<1:
            print("比尔格错误：没有内静")
            return
        if self.exe(0, 100+20*self.Neijing, 10, 24)==0:
            return
        print("比尔格的祝福！")
        self.Neijing = 0
        self.update_status()
    
    def shibai(self):
        self.exe(0, 0, 10, 0)
        print("失败")
        self.update_status()
    
    def exe(self, work_eff, pro_eff, dur_cost, CP_cost):
        if self.now_CP < self.cal_CP_cost(CP_cost):
            print("CP不够！")
            return 0
        self.work_now += self.cal_work(work_eff)
        self.pro_now += self.cal_pro(pro_eff)
        self.Durability_now = min(self.Durability_now - self.cal_dur(dur_cost), self.Config.Durability)
        self.now_CP = min(self.now_CP - self.cal_CP_cost(CP_cost), self.Config.CP)
        self.update_recommend()
        return 1

    def check_buff(self):
        Zhangwo_flag = 0
        Jianyue_flag = 0
        Chongjing_flag = 0
        Gaige_flag = 0
        Kuobu_flag = 0
        
        if self.Zhangwo > 0:
            Zhangwo_flag = 1
        if self.Jianyue > 0:
            Jianyue_flag = 1
        if self.Chongjing > 0:
            Chongjing_flag = 1
        if self.Gaige > 0:
            Gaige_flag = 1
        if self.Kuobu > 0:
            Kuobu_flag = 1
        return (Zhangwo_flag, Jianyue_flag, Chongjing_flag, Gaige_flag, Kuobu_flag)
    
    def cal_work(self,eff):
        (Zhangwo_flag, Jianyue_flag, Chongjing_flag, Gaige_flag, Kuobu_flag) = self.check_buff()
        if_dajinzhan = 0
        if self.ball == DAJINZHAN:
            if_dajinzhan = 1
        self.work = math.floor(0.8* (0.21 * self.Config.Craftsmanship + 2) * (10000 + self.Config.Craftsmanship) / (10000 + 2620.0) * (1 + 0.5 * if_dajinzhan))
        self.work_eff += math.floor(eff* (1 + 0.5*Chongjing_flag) * (1 + 0.5 * if_dajinzhan))
        return math.floor(self.work * eff/100 * (1 + 0.5*Chongjing_flag))
     
    def cal_pro(self,eff):
        (Zhangwo_flag, Jianyue_flag, Chongjing_flag, Gaige_flag, Kuobu_flag) = self.check_buff()
        if_hongqiu = 0
        if self.ball == HONGQIU:
            if_hongqiu= 1
        if eff>0:
            self.Kuobu = 0
        temp_pro_acc = math.floor(self.Config.Control * (1 + 0.2 * max(self.Neijing-1,0)))
        self.pro = math.floor(0.6 * (0.35 * temp_pro_acc + 35) * (10000 + temp_pro_acc) / (10000.0 + 2540.0) * (1 + 0.5 * if_hongqiu))
        return math.floor(self.pro * eff/100.0 * (1 + 0.5 * Gaige_flag + Kuobu_flag))
        
    def cal_dur(self,cost):
        (Zhangwo_flag, Jianyue_flag, Chongjing_flag, Gaige_flag, Kuobu_flag) = self.check_buff()
        if_lanqiu = 0
        if self.ball == LANQIU:
            if_lanqiu = 1
        return math.ceil(cost/(1 + if_lanqiu)/(1 + Jianyue_flag))
    
    def cal_CP_cost(self,cost):
        if_lvqiu = 0
        if self.ball == LVQIU:
            if_lvqiu = 1
        return math.ceil(cost/(1 + if_lvqiu))
        
    def getDataText(self):
        DataText = str(self.work_now) + "/" + str(self.Config.Progress) + "\n"
        DataText += str(self.pro_now) + "/" + str(self.Config.Quality) + "\n"
        DataText += str(self.Durability_now) + "/" + str(self.Config.Durability) + "\n"
        DataText += str(self.now_CP) + "/" + str(self.Config.CP)
        return DataText

    def getBuffText(self):
        BuffText=""
        if self.Neijing > 0:
            BuffText+=" 内静：" + str(self.Neijing)
        if self.Zhangwo > 0:
            BuffText+=" 掌握：" + str(self.Zhangwo)
        if self.Jianyue > 0:
            BuffText+=" 俭约：" + str(self.Jianyue)
        if self.Chongjing > 0:
            BuffText+=" 崇敬：" + str(self.Chongjing)
        if self.Gaige > 0:
            BuffText+=" 改革：" + str(self.Gaige)
        if self.Kuobu > 0:
            BuffText+=" 阔步：" + str(self.Kuobu)
        if self.Guancha > 0:
            BuffText+=" 观察"
        return BuffText
        
    def update_canvas(self):
        self.canvas.coords(self.work_rec,(0, 0, self.work_now/self.Config.Progress*self.window_width, 19))
        self.canvas.coords(self.pro_rec,(0, 20, self.pro_now/self.Config.Quality*self.window_width, 39))
        self.canvas.coords(self.Durability_rec,(0, 40, self.Durability_now/self.Config.Durability*self.window_width, 59))
        self.canvas.coords(self.CP_rec,(0, 60, self.now_CP/self.Config.CP*self.window_width, 80))
        self.master.update()
        
    def recommend(self):
        if self.Neijing < 8 and self.work_eff < self.work_eff_all-120:
            self.Stage = START
        elif self.Neijing < 8 and self.work_eff >= self.work_eff_all-120:
            self.Stage = WORK_FIN
        elif self.work_eff < self.work_eff_all-120:
            self.Stage = PRO_FIN
        else:
            self.Stage = FINISH
            
            
        if self.Stage == START:
            if self.ball == BAIQIU:
                if (self.Durability_now <= 20 and self.Zhangwo == 0 and self.Jianyue == 0) or (self.Durability_now <= 15 and (self.Jianyue > 0 or self.Zhangwo > 0)):
                    return "精修"
                elif self.Chongjing == 0:
                    if self.work_eff < 2250:
                        return "仓促"
                    else:
                        return "最终确认+观察+注视制作"
                        
                elif self.work_eff < 2250:
                    return "高速制作"
                else:
                    return "模范制作"
                    
            if self.ball == HONGQIU:
                if (self.Durability_now <= 10 and self.Jianyue == 0) or (self.Durability_now <= 5 and self.Jianyue > 0):
                    return "秘诀"
                elif self.Chongjing == 0:
                    return "集中加工"
                else:
                    return "集中制作"
                    
            if self.ball == LVQIU:
                if self.Durability_now <= 25:
                    return "精修"
                elif self.Zhangwo == 0:
                    return "掌握"
                elif self.Jianyue == 0:
                    return "长期俭约"
                else:
                    return "坯料加工"
                    
            if self.ball == LANQIU:
                if self.Durability_now <= 5 :
                    return "精修"
                elif self.Chongjing == 0:
                    return "仓促"
                elif self.work_eff < 2250:
                    return "高速制作"
                else:
                    return "模范制作"
                    
            if self.ball == DAJINZHAN:
                if (self.Durability_now <= 10 and self.Jianyue == 0) or (self.Durability_now <= 5 and (self.Jianyue > 0)):
                    return "精修"
                else:
                    if self.Chongjing > 0:
                        if self.work_eff < self.work_eff_all - 1175:
                            return "高速制作"
                        elif self.work_eff < 2250:
                            self.now_CP -= 1
                            return "最终确认+高速制作"
                        else:
                            self.now_CP -= 1
                            return "最终确认+模范制作"
                    else:
                        if self.work_eff < 2250:
                            return "高速制作"
                        else:
                            return "模范制作"
            
            if self.ball == CHANGCHIXU:
                if self.Chongjing == 0:
                    return "崇敬"
                else:
                    if (self.Durability_now <= 20 and self.Zhangwo == 0 and self.Jianyue == 0) or (self.Durability_now <= 15 and (self.Jianyue > 0 or self.Zhangwo > 0)):
                        return "精修"
                    elif self.work_eff < 2250:
                        return "高速制作"
                    else:
                        return "模范制作"
            
        if self.Stage == PRO_FIN:
            if self.ball == BAIQIU:
                if (self.Durability_now <= 20 and self.Zhangwo == 0 and self.Jianyue == 0) or (self.Durability_now <= 15 and (self.Jianyue > 0 or self.Zhangwo > 0)):
                    return "精修"
                elif self.Chongjing == 0:
                    if self.work_eff < 2250:
                        return "崇敬"
                    else:
                        return "最终确认+观察+注视制作"
                elif self.work_eff < 2250:
                    return "高速制作"
                else:
                    return "模范制作"
                    
            if self.ball == HONGQIU:
                if (self.Durability_now <= 10 and self.Jianyue == 0) or (self.Durability_now <= 5 and self.Jianyue > 0) or (self.Neijing == 11):
                    return "秘诀"
                elif self.Chongjing == 0:
                    return "集中加工"
                else:
                    return "集中制作"
                    
            if self.ball == LVQIU:
                if self.Durability_now <= 25:
                    return "精修"
                elif self.Zhangwo == 0:
                    return "掌握"
                elif self.Jianyue == 0:
                    return "长期俭约"
                else:
                    return "坯料加工"
                    
            if self.ball == LANQIU:
                if self.Durability_now <= 5 :
                    return "精修"
                elif self.Chongjing == 0:
                    return "崇敬"
                elif self.work_eff < 2250:
                    return "高速制作"
                else:
                    return "模范制作"
                    
            if self.ball == DAJINZHAN:
                if (self.Durability_now <= 10 and self.Jianyue == 0) or (self.Durability_now <= 5 and (self.Jianyue > 0)):
                    return "精修"
                else:
                    if self.Chongjing > 0:
                        if self.work_eff < self.work_eff_all - 1175:
                            return "高速制作"
                        elif self.work_eff < 2250:
                            self.now_CP -= 1
                            return "最终确认+高速制作"
                        else:
                            self.now_CP -= 1
                            return "最终确认+模范制作"
                    else:
                        if self.work_eff < 2250:
                            return "高速制作"
                        else:
                            return "模范制作"
                            
            if self.ball == CHANGCHIXU:
                if self.work_eff > 2250:
                    return "最终确认+观察+注视制作"
                if self.Chongjing == 0:
                    return "崇敬"
                else:
                    if (self.Durability_now <= 20 and self.Zhangwo == 0 and self.Jianyue == 0) or (self.Durability_now <= 15 and (self.Jianyue > 0 or self.Zhangwo > 0)):
                        return "精修"
                    elif self.work_eff < 2250:
                        return "高速制作"
                    else:
                        return "模范制作"
                        
        if self.Stage == WORK_FIN:
            if self.ball == BAIQIU:
                if (self.Durability_now <= 20 and self.Zhangwo == 0 and self.Jianyue == 0) or (self.Durability_now <= 15 and (self.Jianyue > 0 or self.Zhangwo > 0)):
                    return "精修"
                else:
                    return "仓促"
                    
            if self.ball == HONGQIU:
                if (self.Durability_now <= 10 and self.Jianyue == 0) or (self.Durability_now <= 5 and self.Jianyue > 0):
                    return "秘诀"
                else:
                    return "集中加工"
                    
            if self.ball == LVQIU:
                if self.Durability_now <= 25:
                    return "精修"
                elif self.Zhangwo == 0:
                    return "掌握"
                elif self.Jianyue == 0:
                    return "长期俭约"
                else:
                    return "坯料加工"
                    
            if self.ball == LANQIU:
                if self.Durability_now <= 5 :
                    return "精修"
                else:
                    return "仓促"
                    
            if self.ball == DAJINZHAN:
                if (self.Durability_now <= 20 and self.Zhangwo == 0 and self.Jianyue == 0) or (self.Durability_now <= 15 and (self.Jianyue > 0 or self.Zhangwo > 0)):
                    return "精修"
                else:
                    return "仓促"
                    
            if self.ball == CHANGCHIXU:
                if self.Gaige == 0:
                    return "改革"
                else:
                    if (self.Durability_now <= 20 and self.Zhangwo == 0 and self.Jianyue == 0) or (self.Durability_now <= 15 and (self.Jianyue > 0 or self.Zhangwo > 0)):
                        return "精修"
                    else:
                        return "仓促"
            
        if self.Stage == FINISH:
            dur_all = self.Durability_now + self.Zhangwo * 5
            ret_text= "当前等效耐久：" + str(dur_all) + " 当前CP：" + str(self.now_CP) + "\n"
            
            if self.now_CP >= 389 and dur_all + (self.now_CP - 389) // 88 *30 >=56:
                ret_text += "阔步俭约双坯料+俭约加工+阔步坯料比尔格\n"
            elif self.now_CP >= 374 and dur_all + (self.now_CP - 374) // 88 *30 >=46:
                ret_text += "阔步俭约双坯料+俭约加工+阔步注视比尔格\n"
            elif self.now_CP >= 364 and dur_all + (self.now_CP - 364) // 88 *30 >=51:
                ret_text += "阔步俭约双坯料+阔步坯料比尔格\n"
            elif self.now_CP >= 308 and dur_all + (self.now_CP - 308) // 88 *30 >=71:
                ret_text += "阔步双坯料+阔步坯料比尔格\n"
            elif self.now_CP >= 293 and dur_all + (self.now_CP - 293) // 88 *30 >=61:
                ret_text += "阔步双坯料+阔步注视比尔格\n"
            else:
                ret_text +="当前无推荐收尾，自行选择注视吊球或者倒掉重来\n"
            return ret_text
        return "0"
        
    def update_recommend(self):
        self.recommend_label['text'] = "推荐技能：" + self.recommend()
        self.recommend_label.update()
        
    def update_status(self):
        if self.Zhangwo > 0:
            self.Durability_now = min(55,self.Durability_now+5)
    
        self.Zhangwo = max(0, self.Zhangwo-1)
        self.Jianyue = max(0, self.Jianyue-1)
        self.Chongjing = max(0, self.Chongjing-1)
        self.Gaige = max(0, self.Gaige-1)
        self.Guancha = max(0, self.Guancha-1)
        self.Kuobu = max(0, self.Kuobu-1)
        self.Status.Step += 1
        
        self.update_canvas()
        
        self.canvas_data['text'] = self.getDataText()
        self.canvas_data.update()
        
        self.buff_label['text'] = self.getBuffText()
        self.buff_label.update()
        self.update_recommend()
        
    def restart_program(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)
        
root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
