# AutoBuy
三角洲自动抢卡交易行脚本

非开箱即用

有GUI，修改内容后点击保存配置，将GUI拖动到不会遮挡交易行钥匙卡的左侧后点击开始购买即可。

配置文件

user_config.yaml

buy_option: 填写要买的卡/最高购买与最低购买价格

wallet_option: 填写当前的钱包钱数

开始使用

游戏内点到交易行 -> 钥匙 -> 包含你要买的钥匙的那张图

以管理员方式运行main.py，注意cmd窗口不要挡住钥匙区域（可以放在左边）

等待，想停的话按住's'

在https://github.com/DUYA112233/DeltaGrab基础上二次开发

打包后的内容，存在一个问题，会报错utf-8...

Traceback (most recent call last): File "RunBuy.py", line 120, in File "RunBuy.py", line 75, in get_card_name File "pytesseract\pytesseract.py", line 486, in image_to_string File "pytesseract\pytesseract.py", line 489, in File "pytesseract\pytesseract.py", line 352, in run_and_get_output File "pytesseract\pytesseract.py", line 284, in run_tesseract File "pytesseract\pytesseract.py", line 172, in get_errors UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc2 in position 44: invalid continuation byte [PYI-70012:ERROR] Failed to execute script 'RunBuy' due to unhandled exception!

希望可以解决打包后无法运行的问题。
