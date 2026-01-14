from vosk import Model, KaldiRecognizer
import pyaudio
import json
import pyttsx3
import os
import sys
from vosk import Model
import traceback
import pypinyin

def handle_exception(exc_type, exc_value, exc_traceback):
    print("💥 程序崩溃！", file=sys.stderr)
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)

    # 弹窗提示（让用户知道出错了）
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("错误", f"程序启动失败：\n{exc_value}")
    except:
        pass

    # 防止窗口闪退
    if os.isatty(0):
        input("\n按回车键退出...")
    else:
        os.system('echo "\n按回车键退出..."; read')

sys.excepthook = handle_exception

##-----------------------------------
def resource_path(relative_path):
    """ 获取资源在打包后的真实路径 """
    try:
        # PyInstaller 创建的临时文件夹
        base_path = sys._MEIPASS
    except Exception:
        # 开发模式下使用当前目录
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 使用动态路径加载模型
model_path = resource_path("vosk-model-small-cn-0.22")
print(f"Loading model from: {model_path}")  # 调试用，可查看是否路径正确

if not os.path.exists(model_path):
    raise FileNotFoundError(f"模型未找到: {model_path}")

model1 = Model(model_path)


# 使用示例
# img_path = resource_path("logo.png")



def texvoc(n):
    engine = pyttsx3.init()

    # --- 调整语速 ---
    rate = engine.getProperty('rate') # 获取当前语速
    engine.setProperty('rate', 170) # 设置新语速 (默认约200，数值越小越慢)

    # --- 调整音量 ---
    volume = engine.getProperty('volume') # 获取当前音量 (0.0 到 1.0)
    engine.setProperty('volume', 0.9) # 设置音量为 80%

    # --- 切换声音 (男声/女声) ---
    voices = engine.getProperty('voices')
    # 通常 voices[0] 是男声，voices[1] 是女声 (取决于系统安装的语音包)
    for voice in voices:
        if 'zh' in voice.languages:
            print(voice.name,voice.id,voice.languages)
    for voice in voices:
        if  'de_DK' in voice.languages:
            engine.setProperty('voice', voice.id) 
            print(f"\n已切换到中文语音: {voice.name}")
            print('Hello!')
            break
    if n == 1:
        text = "是在叫我吗？大家好，我是小智，不好意思，打了个瞌睡，哈哈"
        engine.say(text)
        engine.runAndWait()
    if n == 2:
        text = "这个我当然知道，向量(Vector)是数学和物理学中的一个基本概念,用来表示既有大小又有方向的量。"
        engine.say(text)
        engine.runAndWait()
    if n == 3:
        print('='*30)
        print('语音识别已启动······')
        print('='*30)
        text = "语音识别以启动······"
        engine.say(text)
        engine.runAndWait()



def offline_recognize():
    # 1. 加载下载好的中文模型
    global model1
    model = model1 # 指向模型文件夹
    
    # 2. 创建识别器
    recognizer = KaldiRecognizer(model, 16000) # 采样率必须匹配
    
    # 3. 配置麦克风流
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
    stream.start_stream()

    print("离线识别已启动，请说话... (按 Ctrl+C 停止)")

    while True:
        # 读取音频数据
        data = stream.read(4000)
        
        # 识别音频
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            # 解析 JSON 结果
            result_json = json.loads(result)
            text = result_json.get('text', '')
            if text:
                print(f"离线识别结果: {text}")
                if '所致' in text or '下坠' in text or '小智' in text or '嫂子' in text or '小姐' in text or '小猪' in text or '下车' in text or '小镇' in text or '小吃' in text or '下去' in text or ('xiao' in pypinyin.lazy_pinyin(text) and 'zhi' in pypinyin.lazy_pinyin(text)):
                    n = 1
                    texvoc(n)
                    break   
                if '想要' in text or '项链' in text or '想念' in text or '下来' in text or '香料' in text or'向量' in text or '商量' in text or ('xiang' in pypinyin.lazy_pinyin(text) and 'liang' in pypinyin.lazy_pinyin(text)):
                    n = 2
                    texvoc(n)
                    break
                    

                # break # 识别到一句话后退出，实际使用中可去掉
texvoc(3)
offline_recognize()
offline_recognize()


## pyinstaller -F -w -i favicon.ico main.py
## pyinstaller --add-data 'vosk-model-small-cn-0.22:vosk-model-small-cn-0.22' -F -i /Users/a3/Desktop/python大数据分析/数模PPT/wei.jpg /Users/a3/Desktop/python大数据分析/数模PPT/Hello.py


## pyinstaller --icon=/Users/a3/Desktop/new/wei.jpg --add-binary "/Users/a3/Desktop/信息/.venv/lib/python3.10/site-packages/vosk/libvosk.dyld:vosk" --add-data "vosk-model-small-cn-0.22:vosk-model-small-cn-0.22" -F -w /Users/a3/Desktop/python大数据分析/数模PPT/Hello.py

##pyinstaller --icon=/Users/a3/Desktop/new/AppIcon.icns --add-binary "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/vosk/libvosk.dyld:vosk" --add-data "vosk-model-small-cn-0.22:vosk-model-small-cn-0.22" -F /Users/a3/Desktop/new/Hello.py

##-------
##  vosk 安装路径查询 python3 -c "import vosk; import os; print(os.path.dirname(vosk.__file__))"
## /Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/vosk