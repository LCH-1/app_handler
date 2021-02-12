import subprocess
import shutil
import zipfile
import random
import os
import sys
import queue
import threading
from time import sleep
from tkinter import *
try:
    from TkinterDnD2 import *
except:
    print("-error- TkinterDnD2 폴더를 $Python\\Lib\\site-packages\\ 경로에 넣어주세요.\n 파일 없으면 chlee한데 받으세영")
    sleep(10)
    sys.exit(0)
    pass

#adb zipalign apksigner aapt java


# zipalignPath = "C:\\Users\\USER\\AppData\\Local\\Android\\Sdk\\build-tools\\29.0.3\\zipalign.exe"
# apksignerPath = "C:\\Users\\USER\\AppData\\Local\\Android\\Sdk\\build-tools\\29.0.3\\apksigner.bat"
class GuiPart:
    def __init__(self, app, queue, start_thread, execute_command, get_apk_info):
        self.queue = queue
        self.app = app
        # self.txtbox = Text(root)
        # self.txtbox.pack()
        self.execute_command = execute_command
        # btn = Button(master, text='Quit', command=args[0][0])
        # btn.pack(expand=True)
        self.is_func_executing = False
        func_commands = ["adb", "zipalign", "apksigner", "aapt", "java"]
        notfound_string = "내부 또는 외부 명령, 실행할 수 있는 프로그램, 또는"
        self.apksignerPath = "apksigner"
        self.zipalignPath  = "zipalign"
        for func_command in func_commands:
            result = execute_command(func_command, 2)
            for line in result:
                if notfound_string in line and func_command == "apksigner":
                    self.apksignerPath = os.path.dirname(os.path.realpath(__file__)) + "\\bin\\apksigner.bat"
                elif notfound_string in line and func_command == "zipalign":
                    self.zipalignPath  = os.path.dirname(os.path.realpath(__file__)) + "\\bin\\zipalign.exe"
                elif notfound_string in line:
                    print(f"{func_command}이(가) 없거나 환경변수가 설정되지 않았습니다.")
                    sys.exit(0)

        try: 
            self.apk_path = self.sys.argv[1]
            apk_info = get_apk_info(apk_path)

            self.package_name = apk_info["pkg"]
            self.app_version = apk_info["verName"]
            self.launchable_activity = apk_info["lnchActv"]
        except:
            self.apk_path = "apk를 드래그 해주세요"
            self.package_name = ""
            self.app_version = ""
            self.launchable_activity = ""

        

        is_device_connect = False
    # apk_path = "C:\\Users\\USER\\Desktop\\myscript\\python\\normal2.apk"
        self.device_connect_status = Label(app, bg = 'gray27', fg = "white", font = ('Arial','10','bold'), text = "device is not connected")
        self.device_connect_status.grid(row = 99, column = 2, columnspan = 3,sticky = W)
        device_status_check_thread = threading.Thread(target = self.check_device_connect, args=(), daemon = True)
        device_status_check_thread.start()

        left_blank = Label(app, text = "", bg='gray27')
        left_blank.grid(row = 0, column = 0, ipadx = 8) #왼쪽 / 위 공백 생성
        right_blank = Label(app, text = "", bg='gray27')
        right_blank.grid(row = 101, column = 101, ipadx = 1) #오른쪽 / 아래 공백 생성
        bt_blank1 = Label(app, text = "", bg='gray27')
        bt_blank1.grid(row = 100, column = 3, ipadx = 2, ipady = 10) #홈 / back 사이 공백

        self.func1_bt = Button(app, text = "루팅 탐지 시작(ART 생성)", width = '23', bg='gray18', fg = "white", font = ('Arial','10','bold'), command = lambda: start_thread(self.apk_path, 1))
        self.func1_bt.grid(row = 1, column = 2, columnspan = 3, pady = 2)
        self.func2_bt = Button(app, text = "루팅 탐지 끝(ART 삭제)", width = '23', bg='gray18', fg = "white", font = ('Arial','10','bold'), command = lambda: start_thread(self.apk_path, 2))
        self.func2_bt.grid(row = 2, column = 2, columnspan = 3, pady = 2)
        self.func3_bt = Button(app, text = "apk 리사이닝", width = '23', bg='gray18', fg = "white", font = ('Arial','10','bold'), command = lambda: start_thread(self.apk_path, 3))
        self.func3_bt.grid(row = 3, column = 2, columnspan = 3, pady = 2)
        self.func4_bt = Button(app, text = "apk 위변조", width = '23', bg='gray18', fg = "white", font = ('Arial','10','bold'), command = lambda: start_thread(self.apk_path, 4))
        self.func4_bt.grid(row = 4, column = 2, columnspan = 3, pady = 2)
        self.func5_bt = Button(app, text = "apk 정보 확인", width = '23', bg='gray18', fg = "white", font = ('Arial','10','bold'), command = lambda: start_thread(self.apk_path, 5))
        self.func5_bt.grid(row = 5, column = 2, columnspan = 3, pady = 2)
        self.func6_bt = Button(app, text = "apk 삭제", width = '23', bg='gray18', fg = "white", font = ('Arial','10','bold'), command = lambda: start_thread(self.apk_path, 6))
        self.func6_bt.grid(row = 6, column = 2, columnspan = 3, pady = 2)
        self.func7_bt = Button(app, text = "apk 설치", width = '23', bg='gray18', fg = "white", font = ('Arial','10','bold'), command = lambda: start_thread(self.apk_path, 7))
        self.func7_bt.grid(row = 7, column = 2, columnspan = 3, pady = 2)
        self.func8_bt = Button(app, text = "앱 실행", width = '23', bg='gray18', fg = "white", font = ('Arial','10','bold'), command = lambda: start_thread(self.apk_path, 8))
        self.func8_bt.grid(row = 8, column = 2, columnspan = 3, pady = 2)
        self.func9_bt = Button(app, text = "앱 종료", width = '23', bg='gray18', fg = "white", font = ('Arial','10','bold'), command = lambda: start_thread(self.apk_path, 9))
        self.func9_bt.grid(row = 9, column = 2, columnspan = 3, pady = 2)

        self.txtbox = Text(app, width=60, height=25, bg='black', fg = "white", font = ('Arial','10','bold'))
        # self.txtbox = Text(app, width=60, height=22, bg='black', fg = "white", font = ('Arial','10','bold'))
        self.txtbox.grid(row = 1, column = 100, rowspan = 100, padx = 15, pady = 3, sticky = N)
        self.txtbox.config(state=DISABLED)


        # self.cmdbox_sv = StringVar()
        # self.cmdbox_sv.set('===change apk, drop apk file here===')
        # self.cmdbox = Entry(app, textvar=self.cmdbox_sv, width=60, bg='black', fg = "white", font = ('Arial','10','bold'))
        # self.cmdbox.grid(row = 99, column = 100, rowspan = 100, padx = 15, pady = 0)
        # self.cmdbox.bind("<Return>", self.input_enter)
        self.txtbox.drop_target_register(DND_FILES)
        self.txtbox.dnd_bind('<<Drop>>', self.drop)

        self.home_bt = Button(app, text = "home", width = '10', bg='gray18', fg = "white", font = ('Arial','10','bold'), command = lambda: start_thread(self.apk_path, 10))
        self.home_bt.grid(row = 100, column = 2,)
        self.back_bt = Button(app, text = "back", width = '10', bg='gray18', fg = "white", font = ('Arial','10','bold'), command = lambda: start_thread(self.apk_path, 11))
        self.back_bt.grid(row = 100, column = 4)

        self.apk_file_name = Label(app, bg = 'gray27', fg = "white", font = ('Arial','10','bold'), text = self.apk_path.split("\\")[-1])
        self.apk_file_name.grid(row = 97, column = 2, columnspan = 3,sticky = W)
        self.app_package_info = Label(app, bg = 'gray27', fg = "white", font = ('Arial','10','bold'), text = self.package_name + " / " + self.app_version)
        self.app_package_info.grid(row = 98, column = 2, columnspan = 3,sticky = W)


        self.queue.put("여기에 apk를 드래그 하면 선택된 apk를 변경할 수 있습니다." + "\n")

    def check_device_connect(self):
        global is_device_connect
        while True:
            is_device_connect = self.isDeviceConnected()
            if is_device_connect:
                is_device_connect = True
                self.device_connect_status['text'] = "device is connected"
            else:
                is_device_connect = False
                self.device_connect_status['text'] = "device is not connected"
            sleep(0.5)

    def isDeviceConnected(self):
        result = self.execute_command("adb devices", 2)
        if "\tdevice" in result[1]: return True
        else: return False


    def process_incoming(self):
        """ Handle all messages currently in the queue. """
        while self.queue.qsize():
            try:
                info = self.queue.get_nowait()
                self.txtbox.config(state=NORMAL)
                self.txtbox.insert(END, info)
                self.txtbox.config(state=DISABLED)
            except queue.Empty:  # Shouldn't happen.
                pass

    # def input_enter(self, event):
    #     self.txtbox.delete('1.0', END)
    #     input_command = str(self.cmdbox.get())
    #     self.execute_command(input_command, 1)
    #     self.cmdbox.delete(0, END)

    def drop(self, event):
        if self.is_func_executing:
            self.queue.put("기능 실행 중에는 apk를 변경할 수 없습니다." + "\n")
            return
        # self.cmdbox_sv.set(event.data)
        self.txtbox.config(state=NORMAL)
        self.txtbox.delete('1.0', END)
        self.txtbox.config(state=DISABLED)
        if event.data[-4:] != ".apk":
            self.queue.put("apk 파일이 아닙니다.\n")
            return

        self.apk_path = event.data
        result = self.execute_command("aapt dump badging \"{}\"".format(self.apk_path), 2)
        for line in result:
            if "package: name=" in line:
                self.package_name = line.split(' ')[1].replace("name=", '').replace("'", '')
                self.app_version = line.split(" ")[3].split("\\r")[0].replace("versionName=", "").replace("'", "")
                # break
            elif "launchable-activity: name=" in line: 
                    self.launchable_activity = line.split(' ')[1].replace("name=", '').replace("'", '')
                    # print(self.launchable_activity)
            elif "Illegal byte sequence" in line:
                self.queue.put("앱 정보를 확인할 수 없습니다. 경로에 한글이 포함되어 있다면 삭제해주세요" + "\n")
                break

        self.apk_file_name['text'] = self.apk_path.split("/")[-1]
        self.app_package_info['text'] = self.package_name + " / " + self.app_version

        self.queue.put("선택된 apk 파일이 변경되었습니다.\n")
        self.queue.put(f"apk path : {self.apk_path}\n")

class ThreadedClient:
    """ Launch the main part of the GUI and the worker thread.
        periodic_call() and end_application() could reside in the GUI part, but
        putting them here keeps all the thread controls in a single place.
    """
    def __init__(self, master):
        self.master = master
        self.queue = queue.Queue()

        # Set up the GUI part.
        self.gui = GuiPart(master, self.queue, self.start_thread, self.execute_command, self.get_apk_info)
        self.periodic_call(100)
        # Set up the background processing thread.

    def start_thread(self, apk_path, func_num):
        self.thread = threading.Thread(target=self.start_func, args=(apk_path, func_num,), daemon = True)
        self.thread.start()

        # Start periodic checking of the queue.
        

    def periodic_call(self, delay):
        """ Every delay ms process everything new in the queue. """
        self.gui.process_incoming()
        self.master.after(delay, self.periodic_call, delay)

    # Runs in separate thread - NO tkinter calls allowed.

    def start_func(self, apk_path, func_num):
        self.gui.is_func_executing = True

        if func_num not in [10, 11] :
            self.button_disable();
            self.gui.txtbox.config(state=NORMAL)
            self.gui.txtbox.delete('1.0', END)
            self.gui.txtbox.config(state=DISABLED)
        
        if func_num == 1: self.startRootTest()
        if func_num == 2: self.endRootTest()
        if func_num == 3: self.resignApkWithZipalign(apk_path)
        if func_num == 4: self.integrityApk(apk_path)
        if func_num == 5: self.checkapk_info(apk_path)
        if func_num == 6: self.removeApk(apk_path)
        if func_num == 7: self.startInstall(apk_path)
        if func_num == 8: self.appStart(apk_path)
        if func_num == 9: self.appStop(apk_path)
        if func_num == 10: self.press_bt_home()
        if func_num == 11: self.press_bt_back()
        
        if func_num not in [10, 11] : self.button_normal()
        # app.after(1, lambda: button_normal())
        self.gui.is_func_executing = False

    def execute_command(self, cmd, optionNum = 0, **kwargs):
        if optionNum == 2: 
            pass

        elif kwargs.get("change_path", False):
            self.queue.put(cmd.replace(kwargs["dst"], kwargs["src"]) + "\n")
        
        else:
            self.queue.put(cmd + "\n")

        spc = subprocess.Popen(cmd, shell=True, bufsize=256, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        encoding_names = ["ascii", "cp949", "utf-8", "euc-kr"]
        result = None
        for name in encoding_names:
            try:
                result = bytes(spc.communicate()[0]).decode(name).split("\r\n")
            except UnicodeDecodeError:
                continue

        if optionNum == 1:
            for line in result:
                self.queue.put(line + "\n")
                # print(result)
        return result

    def removeSignInfo(self, apk_path):
        outputApk = apk_path[:-4] + "_sign.apk"
        with zipfile.ZipFile(apk_path, 'r') as zipIn:
            with zipfile.ZipFile(outputApk, 'w') as zipOut:
                for item in zipIn.infolist():
                    buffer = zipIn.read(item.filename)
                    if item.filename == "META-INF\\MANIFEST.MF" or item.filename == "META-INF/MANIFEST.MF" :
                        self.queue.put("remove " + item.filename + "\n")
                    else: 
                        zipOut.writestr(item, buffer)
        return outputApk

    def zipalign(self, apk_path, nameset = 0):
        self.execute_command('{} -v 4 "{}" "{}"'.format(self.gui.zipalignPath, apk_path, apk_path[:-4] + "_sign.apk"))

        self.queue.put("zipalign..." + "\n")
        if nameset == 0:
            os.remove(apk_path)
            os.rename(apk_path[:-4] + "_sign.apk", apk_path)
            return apk_path
        else: return apk_path[:-4] + "_sign.apk"


    def resign(self, apk_path):
        keyPass = "qwer1234"
        keyStoreAlias = "test"
        keyStorePass = "qwer1234"
        result = self.execute_command("{} sign --ks {}\\lib\\sign.jks --key-pass pass:{} --ks-key-alias {}"
                                    " --ks-pass pass:{} \"{}\"".format(self.gui.apksignerPath, os.path.dirname(os.path.realpath(__file__)), 
                                                                        keyPass, keyStoreAlias, keyStorePass, apk_path))
        self.queue.put("resign..." + "\n")
        for i in result:
            if "java.io.FileNotFoundException" in i:
                self.queue.put("sign.jks 파일이 존재하지 않습니다." + "\n")
                return
        self.queue.put("\n{} sign is done".format(apk_path).split("\\")[-1] + "\n")

    def modifySo(self, startPath, outputApk):
        try: 
            os.remove("{}{}META-INF\\MANIFEST.MF".format(startPath, os.sep))
            self.queue.put("remove signInfo", "{}{}META-INF\\MANIFEST.MF".format(startPath, os.sep) + "\n")
        except: 
            self.queue.put("MANIFEST.MF 파일이 존재하지 않습니다." + "\n")
        cpuList = ["armeabi", "armeabi-v7a", "arm64-v8a", "mips", "x86", "x86_64"]
        isExist = False
        soList = {}
        for cpu in cpuList: soList[cpu] = []
        for dirPath, dirs, files in os.walk(startPath):
            for f in files:
                fullPath = "{}{}{}".format(dirPath, os.sep, f)
                if f[-3:] == ".so" and "libAppSuit.so" not in f :
                    for cpu in cpuList:
                        if "{}\\".format(cpu) in fullPath: 
                            soList[cpu].append(fullPath)
        for cpu in cpuList:
            try: 
                randomSo = soList[cpu][random.randrange(0, len(soList[cpu]))]
                isExist = True
            except: 
                self.queue.put("{}에 so 없음".format(cpu) + "\n")
                continue
            with open(randomSo, "a") as modifySo:
                modifySo.write("\nappsuit modify so test!!")
                self.queue.put("{} is modify".format(randomSo) + "\n")
        if not isExist: 
            self.queue.put("so파일이 없어 변조되지 않았습니다." + "\n")
            return False

        return outputApk

    def modifyRes(self, startPath, outputApk):
        os.remove("{}{}META-INF\\MANIFEST.MF".format(startPath, os.sep))
        self.queue.put("remove signInfo", "{}{}META-INF\\MANIFEST.MF".format(startPath, os.sep) + "\n")
        for dirPath, dirs, files in os.walk(startPath):
            for f in files:
                fullPath = "{}{}{}".format(dirPath, os.sep, f)
                if "{}{}res{}".format(startPath, os.sep, os.sep) in fullPath:
                    isModify = True
                    with open(fullPath, "a") as modifyRes: 
                        modifyRes.write("\nappsuit modify so test!!")
                    self.queue.put("{} is modify".format(fullPath) + "\n")
                    return

    def zipApk(self, folderInput, outputApk):
        self.queue.put("zip apk..." + "\n")
        with zipfile.ZipFile(outputApk, 'w') as zip:
            for dirPath, dirs, files in os.walk(folderInput):
                for file in files:
                    # self.queue.put(file + "\n")
                    if "{}\\{}".format(dirPath, file) == "META-INF\\MANIFEST.MF":
                        self.queue.put("remove META-INF\\MANIFEST.MF" + "\n")
                    else: 
                        zip.write(os.path.join(dirPath, file), # 파일 이름
                            os.path.relpath(os.path.join(dirPath, file), folderInput), # 압축 파일의 이름(Default : 파일 이름과 같음)
                            compress_type = zipfile.ZIP_DEFLATED) # 압축 타입

    def unZipApk(self, apk_path, outputPath):
        self.queue.put("unzip {} to {}".format(apk_path, outputPath) + "\n")
        self.execute_command("md {}".format(outputPath), 2)
        with zipfile.ZipFile(apk_path, 'r') as zipIn:
            zipIn.extractall(outputPath)



    def startRootTest(self):
        if not is_device_connect:
            self.queue.put("디바이스가 연결되지 않았습니다." + "\n")
            return

        self.execute_command("adb shell touch /sdcard/APPSUIT_ROOTING_TEST")
        self.queue.put("done" + "\n")

    def endRootTest(self):
        if not is_device_connect:
            self.queue.put("디바이스가 연결되지 않았습니다." + "\n")
            return
        self.execute_command("adb shell rm -rf /sdcard/APPSUIT_ROOTING_TEST")
        self.queue.put("done" + "\n")


    def resignApkWithZipalign(self, apk_path):
        # self.queue.put("resign", apk_path + "\n")
        apk_path = self.removeSignInfo(apk_path)
        outputApk = self.zipalign(apk_path)
        self.resign(outputApk)

    def integrityApk(self, apk_path):
        
        # func8_bt.config(state = "disabled")

        outputSoModApk = apk_path[:-4] + "_so_modify.apk"
        outputSoModDir = "modify_so"

        outputResModApk = apk_path[:-4] + "_res_modify.apk"
        outputResModDir = "modify_res"

        self.unZipApk(apk_path, outputResModDir)
        self.unZipApk(apk_path, outputSoModDir)
        self.modifyRes(outputResModDir, outputResModApk)
        isExist = self.modifySo(outputSoModDir, outputSoModApk)
        self.zipApk(outputResModDir, outputResModApk)
        if isExist: self.zipApk(outputSoModDir, outputSoModApk)

        self.zipalign(outputResModApk)
        if isExist: self.zipalign(outputSoModApk)

        self.resign(outputResModApk)
        if isExist: self.resign(outputSoModApk)

        shutil.rmtree(outputResModDir)
        shutil.rmtree(outputSoModDir)

    def checkapk_info(self, apk_path):
        self.queue.put("apk 정보\n")
        isAppsuit = 0
  
        apk_info = self.get_apk_info(apk_path)
        self.queue.put(f"  package name		: {apk_info['pkg']}\n")
        self.queue.put(f"  version name		: {apk_info['verName']}\n")
        self.queue.put(f"  version code		: {apk_info['verCode']}\n")
        self.queue.put(f"  launchable-activity	: {apk_info['lnchActv']}\n")
        
        with zipfile.ZipFile(apk_path, 'r') as zipIn:
            for f in zipIn.infolist():
                if "assets/appsuit/" in f.filename or "assets\\appsuit\\" in f.filename:
                    isAppsuit = 1
                if "libAppSuit.so" in f.filename:
                    isAppsuit = 2
                    break

        if isAppsuit == 0: self.queue.put("앱수트가 적용되지 않은 앱입니다.\n")
        else: self.queue.put("앱수트 {}차 적용된 앱입니다.\n".format(isAppsuit))

    def get_apk_info(self, apk_path):
        if len(re.compile('[^\u3131-\u3163\uac00-\ud7a3]+').sub('', apk_path)) >= 1:
            desapk_path = self.randomStrGenerator(20) + "_tmp.apk"
            os.rename(apk_path, desapk_path)
            result = self.execute_command("aapt dump badging \"{}\"".format(desapk_path), 2, change_path=True, src=apk_path, dst=desapk_path)
            os.rename(desapk_path, apk_path)
        
        else:
            result = self.execute_command("aapt dump badging \"{}\"".format(apk_path))

        apk_info = {}

        for line in result:
            if "package: name="             in line: apk_info["pkg"]      = line.split(' ')[1].replace("name=", '').replace("'", '')
            if "package: name="             in line: apk_info["verName"]  = line.split(" ")[3].split("\\r")[0].replace("versionName=", "").replace("'", "")
            if "package: name"              in line: apk_info["verCode"]  = line.split(" ")[2].replace("versionCode=", "").replace("'", "")
            if "launchable-activity: name=" in line: apk_info["lnchActv"] = line.split(' ')[1].replace("name=", '').replace("'", '')
            if "Illegal byte sequence"      in line: return False

        return apk_info

    def randomStrGenerator(self, str_len):
        random_string_form = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        random_string = "".join(random.choice(random_string_form) for x in range(str_len))
        return random_string


    def removeApk(self, apk_path):
        if not is_device_connect:
            self.queue.put("디바이스가 연결되지 않았습니다." + "\n")
            return

        result = self.execute_command("aapt dump badging \"{}\"".format(apk_path), 2)
        for line in result:
            if "package: name=" in line:
                package_name = line.split(' ')[1].replace("name=", '').replace("'", '')
                break
            if "Illegal byte sequence" in line: self.queue.put("앱 정보를 확인할 수 없습니다. 경로에 한글이 포함되어 있다면 삭제해주세요" + "\n"); return
        result = self.execute_command("adb uninstall \"{}\"".format(package_name))
        for line in result:
            if "DELETE_FAILED_INTERNAL_ERROR" in line: 
                self.queue.put("앱이 설치되어 있지 않습니다." + "\n")
                return
        self.queue.put("done")

    def installApp(self, apk_path):
        return self.execute_command("adb install -r \"{}\"".format(apk_path))

    def appStart(self, apk_path):
        if not is_device_connect:
            self.queue.put("디바이스가 연결되지 않았습니다." + "\n")
            return
        # result = self.execute_command("aapt dump badging \"{}\"".format(apk_path), 2)
        # for line in result:
        #     if "package: name="             in line: package_name         = line.split(' ')[1].replace("name=", '').replace("'", '')
        #     if "launchable-activity: name=" in line: launchable_activity = line.split(' ')[1].replace("name=", '').replace("'", '')
        result = self.execute_command(f"adb shell am start -n {self.gui.package_name}/{self.gui.launchable_activity}")
        for line in result:
            if "currently running top-most instance." in line:
                self.queue.put("이미 실행중입니다." + "\n")
                return
            elif "does not exist." in line:
                self.queue.put("앱이 설치되어 있지 않습니다. (설치되어 있다면 디버깅 필요)" + "\n")
                return

        self.queue.put("done" + "\n")

    def appStop(self, apk_path):
        if not is_device_connect:
            self.queue.put("디바이스가 연결되지 않았습니다." + "\n")
            return
        # result = self.execute_command("aapt dump badging \"{}\"".format(apk_path), 2)
        # for line in result:
        #     if "package: name=" in line:
        #         package_name = line.split(' ')[1].replace("name=", '').replace("'", '')
        #         break
        #     if "Illegal byte sequence" in line: self.queue.put("앱 정보를 확인할 수 없습니다. 경로에 한글이 포함되어 있다면 삭제해주세요" + "\n"); return
        result = self.execute_command("adb shell am force-stop \"{}\"".format(self.gui.package_name))
        self.queue.put("done" + "\n")

    def signingVerify(self, apk_path):
        result = self.execute_command("{} verify {}".format(self.gui.apksignerPath, apk_path), 2)
        for line in result:
            if "ERROR" in line: 
                for line2 in result: self.queue.put(line2 + "\n")
                self.queue.put("사이닝 되지 않은 apk입니다." + "\n")
                return False
        return True


    def startInstall(self, apk_path):
        if not is_device_connect:
            self.queue.put("디바이스가 연결되지 않았습니다." + "\n");
            return

        for _ in range(3):
            result = self.installApp(apk_path)
            for line in result:
                if "INSTALL_FAILED_VERSION_DOWNGRADE" in line:
                    self.queue.put("\n*** INSTALL_FAILED_VERSION_DOWNGRADE 에러로 설치 불가 ***" + "\n")
                    self.queue.put("앱 삭제 후 재설치 됩니다.\n" + "\n")
                    self.removeApk("{}".format(apk_path))
                    # return True
                    break

                elif "INSTALL_FAILED_UPDATE_INCOMPATIBLE" in line:
                    self.queue.put("\n*** INSTALL_FAILED_UPDATE_INCOMPATIBLE 에러로 설치 불가 ***" + "\n")
                    self.queue.put("앱 삭제 후 재설치 됩니다.\n" + "\n")
                    self.removeApk("{}".format(apk_path))
                    # return True
                    break

                elif "INSTALL_PARSE_FAILED_NO_CERTIFICATES" in line or "INSTALL_PARSE_FAILED_UNEXPECTED_EXCEPTION" in line:
                    self.queue.put("\n*** INSTALL_PARSE_FAILED_NO_CERTIFICATES 에러로 설치 불가 ***" + "\n")
                    self.queue.put("앱 리사이닝 후 재설치됩니다.\n" + "\n")
                    self.resignApkWithZipalign(apk_path)
                    apk_path = apk_path[:-4] + "_sign.apk"
                    
                    break

                elif "Success" in line:
                    self.queue.put("Success" + "\n")
                    self.appStart(apk_path)
                    isSuccess = True
                    return True
                else:
                    for line2 in result:
                        self.queue.put(line2 + "\n")
                    isSuccess = True
                    return False

    def button_disable(self):
    # self.queue.put("startRootTest" + "\n")
        self.gui.func1_bt.config(state = DISABLED)
        self.gui.func2_bt.config(state = DISABLED)
        self.gui.func3_bt.config(state = DISABLED)
        self.gui.func4_bt.config(state = DISABLED)
        self.gui.func5_bt.config(state = DISABLED)
        self.gui.func6_bt.config(state = DISABLED)
        self.gui.func7_bt.config(state = DISABLED)
        self.gui.func8_bt.config(state = DISABLED)
        self.gui.func9_bt.config(state = DISABLED)
        # home_bt.config(state = DISABLED)
        # back_bt.config(state = DISABLED)

    def button_normal(self):
        self.gui.func1_bt.config(state = NORMAL)
        self.gui.func2_bt.config(state = NORMAL)
        self.gui.func3_bt.config(state = NORMAL)
        self.gui.func4_bt.config(state = NORMAL)
        self.gui.func5_bt.config(state = NORMAL)
        self.gui.func6_bt.config(state = NORMAL)
        self.gui.func7_bt.config(state = NORMAL)
        self.gui.func8_bt.config(state = NORMAL)
        self.gui.func9_bt.config(state = NORMAL)
        # home_bt.config(state = NORMAL)
        # back_bt.config(state = NORMAL)

    def press_bt_back(self):
        if not is_device_connect:
            self.queue.put("디바이스가 연결되지 않았습니다." + "\n")
            return
        self.gui.back_bt.config(state = DISABLED)
        self.gui.home_bt.config(state = DISABLED)

        self.queue.put("press back button" + "\n")
        self.execute_command("adb shell input keyevent 4", 2)
        # self.queue.put("done" + "\n");

        self.gui.back_bt.config(state = NORMAL)
        self.gui.home_bt.config(state = NORMAL)

    def press_bt_home(self):
        if not is_device_connect:
            self.queue.put("디바이스가 연결되지 않았습니다." + "\n")
            return
        self.gui.back_bt.config(state = DISABLED)
        self.gui.home_bt.config(state = DISABLED)

        self.queue.put("press home button" + "\n")
        self.execute_command("adb shell input keyevent 3", 2)
        # self.queue.put("done" + "\n");

        self.gui.back_bt.config(state = NORMAL)
        self.gui.home_bt.config(state = NORMAL)

try:
    root = TkinterDnD.Tk()
except:
    print("-error- tkdnd2.8 폴더를 $Python\\tcl\\ 경로에 넣어주세요.\n 파일 없으면 chlee한데 받으세영")
    sleep(10)
    sys.exit(0)


root.title('android function')
client = ThreadedClient(root)

root.resizable(width=False, height=False)
root.configure(bg='gray27')
root.mainloop()
root.mainloop()
