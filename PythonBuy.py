import os
import tkinter as tk
from tkinter import messagebox
import yaml
import sys
import subprocess
import cv2
import numpy as np
import pyautogui
import time
import pytesseract
from difflib import SequenceMatcher
import keyboard
from pickle import INT

class BuyBotGUI:
    def __init__(self, master):
        self.master = master
        master.title("自动购买卡牌配置工具")
        master.geometry("217x237")
        
        # 创建输入框和标签
        self.create_widgets()
        
        # 检查配置文件是否存在，如果存在则加载
        if os.path.exists('user_config.yaml'):
            self.load_config()
    
    def create_widgets(self):
        # 卡牌名称
        tk.Label(self.master, text="卡牌名称:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.card_name_entry = tk.Entry(self.master, width=15)
        self.card_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # 最低价格（千为单位）
        tk.Label(self.master, text="最低价格:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.min_price_entry = tk.Entry(self.master, width=15)
        self.min_price_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # 最高价格（千为单位）
        tk.Label(self.master, text="最高价格:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.max_price_entry = tk.Entry(self.master, width=15)
        self.max_price_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # 钱包余额阈值
        tk.Label(self.master, text="钱包余额:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.wallet_threshold_entry = tk.Entry(self.master, width=15)
        self.wallet_threshold_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # 钱包余额单位
        tk.Label(self.master, text="余额单位:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.wallet_threshold_key_entry = tk.Entry(self.master, width=15)
        self.wallet_threshold_key_entry.grid(row=4, column=1, padx=2, pady=5)
        
        # 保存配置按钮
        self.save_button = tk.Button(self.master, text="保存配置", command=self.save_config)
        self.save_button.grid(row=5, column=0, columnspan=1, padx=5, pady=5)
        
        # 开始按钮
        self.start_button = tk.Button(self.master, text="开始购买", command=self.start_buy_bot, bg='green', fg='white')
        self.start_button.grid(row=5, column=1, columnspan=1, padx=50, pady=5)
        
        # 状态标签
        self.status_label = tk.Label(self.master, text="", fg='blue')
        self.status_label.grid(row=6, column=0, columnspan=1, pady=5)
        
        # 提示标签
        self.status_label2 = tk.Label(self.master, text="商品价格单位为(千)", fg='blue')
        self.status_label2.grid(row=6, column=1, columnspan=1, pady=5)
    
    def load_config(self):
        try:
            with open('user_config.yaml', 'r', encoding='utf-8') as fin:
                user_configs = yaml.load(fin, Loader=yaml.FullLoader)
                
                # 填充输入框
                moneys = int(user_configs['wallet_option']['now_money'])
                if (
                    user_configs['wallet_option']['now_money_key'] == "m"
                ):
                    moneys = moneys / 1000
                self.card_name_entry.insert(0, user_configs['buy_option']['buy_card_name'])
                self.min_price_entry.insert(0, str(user_configs['buy_option']['buy_price_min']))
                self.max_price_entry.insert(0, str(user_configs['buy_option']['buy_price_max']))
                self.wallet_threshold_entry.insert(0, int(moneys))
                self.wallet_threshold_key_entry.insert(0, user_configs['wallet_option']['now_money_key'])
                
                self.status_label.config(text="配置已加载", fg='green')
        except Exception as e:
            messagebox.showerror("错误", f"加载配置文件失败: {str(e)}")
    
    def save_config(self):
        try:
            # 获取输入值
            buy_card_name = self.card_name_entry.get()
            buy_price_min = int(self.min_price_entry.get())
            buy_price_max = int(self.max_price_entry.get())
            now_money = int(self.wallet_threshold_entry.get())
            now_money_key = self.wallet_threshold_key_entry.get()
            
            # 验证输入
            if not buy_card_name:
                raise ValueError("卡牌名称不能为空")
            if not now_money_key:
                raise ValueError("现金单位不能为空")
            if buy_price_min < 0 or buy_price_max < 0 or now_money < 0:
                raise ValueError("价格不能为负数")
            if buy_price_min > buy_price_max:
                raise ValueError("最低价格不能高于最高价格")
            if now_money_key == "m":
                now_money = now_money * 1000
            
            # 创建配置字典
            user_configs = {
                'buy_option': {
                    'buy_card_name': buy_card_name,
                    'buy_price_min': buy_price_min,
                    'buy_price_max': buy_price_max
                },
                'wallet_option': {
                    'now_money': now_money,
                    'now_money_key': now_money_key
                }
            }
            
            # 保存到文件
            with open('user_config.yaml', 'w', encoding='utf-8') as fout:
                yaml.dump(user_configs, fout, allow_unicode=True)
            
            self.status_label.config(text="配置已保存", fg='green')
            messagebox.showinfo("成功", "配置已保存")
            
        except ValueError as ve:
            messagebox.showerror("输入错误", str(ve))
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {str(e)}")
    
    def start_buy_bot(self):
        # 检查配置文件是否存在
        if not os.path.exists('user_config.yaml'):
            messagebox.showerror("错误", "请先保存配置")
            return
        
        try:
            # 启动购买机器人
            BuyBot().run()
            self.status_label.config(text="程序已启动", fg='green')
        except Exception as e:
            messagebox.showerror("错误", f"启动自动购买程序失败: {str(e)}")

class BuyBot:
    def __init__(self):
        # 判断是否打包环境
        self.IS_FROZEN = getattr(sys, 'frozen', False)
        
        # 设置 Tesseract 路径
        if self.IS_FROZEN:
            TESSERACT_CMD = os.path.join(os.path.dirname(sys.executable), "tesseract.exe")
            TESSDATA_PREFIX = os.path.join(os.path.dirname(sys.executable), "tessdata")
        else:
            TESSERACT_CMD = "tesseract"
            TESSDATA_PREFIX = r"C:\Program Files\Tesseract-OCR\tessdata"
        
        # 应用配置
        os.environ["TESSDATA_PREFIX"] = TESSDATA_PREFIX
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
        
        # 加载配置文件
        with open('pre_config.yaml', 'r', encoding='utf-8') as fin:
            self.pre_configs = yaml.load(fin, Loader=yaml.FullLoader)
        
        with open('user_config.yaml', 'r', encoding='utf-8') as fin:
            self.user_configs = yaml.load(fin, Loader=yaml.FullLoader)

    def match_strings(self, correct_strings, error_strings):
        """通过相似度匹配错误字符串与正确卡牌名称"""
        matched_strings = []
        for error_str in error_strings:
            highest_ratio = 0
            matched_str = ""
            for correct_str in correct_strings:
                ratio = SequenceMatcher(None, correct_str, error_str).ratio()
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    matched_str = correct_str
            if highest_ratio > 0.5:
                matched_strings.append(matched_str)
        return matched_strings

    def take_screenshot(self, region=None):
        """截取指定屏幕区域并转为灰度图"""
        screenshot = pyautogui.screenshot(region=region)
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        return screenshot

    def click_position(self, position):
        """模拟鼠标点击指定坐标"""
        pyautogui.moveTo(position[0], position[1], duration=0.1)
        pyautogui.click()

    def show_image(self, image):
        """显示图像（用于调试）"""
        cv2.imshow('image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def get_card_name(self, image):
        """OCR识别卡牌名称（中文）"""
        ret, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        card_name = pytesseract.image_to_string(
            image, 
            lang='chi_sim', 
            config='--psm 13',
            timeout=5,
        ).encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        return card_name.strip()

    def get_card_price(self, image):
        """OCR识别卡牌价格（数字）"""
        ret, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        card_price = pytesseract.image_to_string(
            image, lang='eng', 
            config='--psm 13 -c tessedit_char_whitelist=\'0123456789\''
        )
        card_price = card_price.replace('\n', '').replace(' ', '')
        try:
            return int(card_price)
        except ValueError:
            return sys.maxsize

    def run(self):
        # 步骤1：识别屏幕上所有卡牌的名称
        card_name = []
        screenshot = self.take_screenshot((
            self.pre_configs['coordinate_position']['card_region'][0],
            self.pre_configs['coordinate_position']['card_region'][1],
            self.pre_configs['coordinate_position']['card_pixel'][0] * 3,
            self.pre_configs['coordinate_position']['card_pixel'][1] * 5
        ))

        for i in range(5):
            for j in range(3):
                card_im = screenshot[
                    self.pre_configs['coordinate_position']['card_pixel'][1] * i : self.pre_configs['coordinate_position']['card_pixel'][1] * (i+1),
                    self.pre_configs['coordinate_position']['card_pixel'][0] * j : self.pre_configs['coordinate_position']['card_pixel'][0] * (j + 1)
                ]
                card_name_im = card_im[
                    : self.pre_configs['coordinate_position']['name_pixel'][1],
                    : self.pre_configs['coordinate_position']['name_pixel'][0]
                ]
                card_name.append(self.get_card_name(card_name_im))

        print(card_name)

        # 步骤2：确定当前地图（匹配预配置的卡牌数据库）
        card_name = [
            self.match_strings(self.pre_configs['card_name']['db'], card_name),
            self.match_strings(self.pre_configs['card_name']['cg'], card_name),
            self.match_strings(self.pre_configs['card_name']['ht'], card_name),
            self.match_strings(self.pre_configs['card_name']['bks'], card_name)
        ][
            [
                len(self.match_strings(self.pre_configs['card_name']['db'], card_name)),
                len(self.match_strings(self.pre_configs['card_name']['cg'], card_name)),
                len(self.match_strings(self.pre_configs['card_name']['ht'], card_name)),
                len(self.match_strings(self.pre_configs['card_name']['bks'], card_name))
            ].index(
                max(
                    len(self.match_strings(self.pre_configs['card_name']['db'], card_name)),
                    len(self.match_strings(self.pre_configs['card_name']['cg'], card_name)),
                    len(self.match_strings(self.pre_configs['card_name']['ht'], card_name)),
                    len(self.match_strings(self.pre_configs['card_name']['bks'], card_name))
                )
            )
        ]
        print(card_name)

        # 步骤3：计算目标卡牌的网格索引
        buy_card_index = [
            card_name.index(self.user_configs['buy_option']['buy_card_name']) % 3,
            card_name.index(self.user_configs['buy_option']['buy_card_name']) // 3
        ]
        print(buy_card_index)

        # 步骤4：主循环——监控价格并购买
        running = True
        min_price = sys.maxsize

        while running:
            # 点击目标卡牌位置
            self.click_position([
                self.pre_configs['coordinate_position']['card_region'][0] + 
                self.pre_configs['coordinate_position']['card_pixel'][0] // 2 + 
                self.pre_configs['coordinate_position']['card_pixel'][0] * buy_card_index[0],
                self.pre_configs['coordinate_position']['card_region'][1] + 
                self.pre_configs['coordinate_position']['card_pixel'][1] // 2 + 
                self.pre_configs['coordinate_position']['card_pixel'][1] * buy_card_index[1]
            ])

            # 识别价格区域
            screenshot = self.take_screenshot(region=(
                self.pre_configs['coordinate_position']['price_region'][0],
                self.pre_configs['coordinate_position']['price_region'][1],
                self.pre_configs['coordinate_position']['price_pixel'][0],
                self.pre_configs['coordinate_position']['price_pixel'][1]
            ))
            card_price = self.get_card_price(screenshot)

            # 检查价格是否符合条件
            if (
                card_price <= self.user_configs['buy_option']['buy_price_max'] * 1000 and
                card_price >= self.user_configs['buy_option']['buy_price_min'] * 1000 and
                card_price > 0
            ):
                # 点击购买按钮（价格区域下方60像素）
                self.click_position([
                    self.pre_configs['coordinate_position']['price_region'][0],
                    self.pre_configs['coordinate_position']['price_region'][1] + 60
                ])
                time.sleep(1)

                # 更新最低价格记录
                if min_price > card_price:
                    min_price = card_price
                    print('min_price', min_price)

                # 检查钱包余额
                screenshot = self.take_screenshot((
                    self.pre_configs['coordinate_position']['wallet_region'][0],
                    self.pre_configs['coordinate_position']['wallet_region'][1],
                    self.pre_configs['coordinate_position']['wallet_pixel'][0],
                    self.pre_configs['coordinate_position']['wallet_pixel'][1]
                ))
                wallet_price = self.get_card_price(screenshot)
                if (
                    self.user_configs['wallet_option']['now_money_key'] == "m"
                ):
                    wallet_price = wallet_price * 1000
                print('wallet_price', wallet_price)

                # 判断余额是否足够且不低于阈值
                if (
                    wallet_price < self.user_configs['wallet_option']['now_money'] and
                    wallet_price >= (self.user_configs['wallet_option']['now_money'] - card_price)
                ):
                    print('bought')
                    running = False
                else:
                    continue

            pyautogui.press('esc')
            if keyboard.is_pressed('s'):
                running = False
                print("stop")

if __name__ == "__main__":
    root = tk.Tk()
    gui = BuyBotGUI(root)
    root.mainloop()