import os
import subprocess
import sys
import shutil
import zipfile
import random
import re

apksignerPath = os.path.dirname(os.path.realpath(__file__)) + "\\..\\bin\\apksigner.bat"
zipalignPath  = os.path.dirname(os.path.realpath(__file__)) + "\\..\\bin\\zipalign.exe"

def execute_command(cmd, optionNum = 0,  **kwargs):
    if optionNum == 2: 
        pass
    elif kwargs.get("change_path", False):
        print(cmd.replace(kwargs["dst"], kwargs["src"]))
    
    else:
        print(cmd)

    spc = subprocess.Popen(cmd, shell=True, bufsize=256, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    encoding_names = ["ascii", "cp949", "utf-8", "euc-kr"]
    result = None
    for name in encoding_names:
        try:
            result = bytes(spc.communicate()[0]).decode(name).split("\r\n")
        except UnicodeDecodeError:
            continue

    if optionNum == 1: [print(i) for i in result]
    return result

def removeSignInfo(apkPath):
    outputApk = apkPath[:-4] + "_sign.apk"
    with zipfile.ZipFile(apkPath, 'r') as zipIn:
        with zipfile.ZipFile(outputApk, 'w') as zipOut:
            for item in zipIn.infolist():
                buffer = zipIn.read(item.filename)
                if item.filename == "META-INF\\MANIFEST.MF" or item.filename == "META-INF/MANIFEST.MF" :
                    print("remove " + item.filename)
                else: 
                    zipOut.writestr(item, buffer)
    return outputApk

def zipalign(apkPath, nameset = 0):
    execute_command('{} -v 4 "{}" "{}"'.format(zipalignPath, apkPath, apkPath[:-4] + "_sign.apk"), 2)

    print("zipalign...")
    if nameset == 0:
        os.remove(apkPath)
        os.rename(apkPath[:-4] + "_sign.apk", apkPath)
        return apkPath
    else: return apkPath[:-4] + "_sign.apk"


def resign(apkPath):
    keyPass = "qwer1234"
    keyStoreAlias = "test"
    keyStorePass = "qwer1234"
    result = execute_command("{} sign --ks {}\\sign.jks --key-pass pass:{} --ks-key-alias {}"
                                " --ks-pass pass:{} \"{}\"".format(apksignerPath, os.path.dirname(os.path.realpath(__file__)), 
                                                                    keyPass, keyStoreAlias, keyStorePass, apkPath))
    print("resign...")
    for i in result:
        if "java.io.FileNotFoundException" in i:
            print("sign.jks 파일이 존재하지 않습니다.")
            return
    print("\n{} sign is done".format(apkPath).split("\\")[-1])

def modifySo(startPath, outputApk):
    try: 
        os.remove("{}{}META-INF\\MANIFEST.MF".format(startPath, os.sep))
        print("remove signInfo", "{}{}META-INF\\MANIFEST.MF".format(startPath, os.sep))
    except: print("MANIFEST.MF 파일이 존재하지 않습니다.")
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
        except: print("{}에 so 없음".format(cpu)); continue
        with open(randomSo, "a") as modifySo:
            modifySo.write("\nappsuit modify so test!!")
        print("{} is modify".format(randomSo))
    if not isExist: 
        print("so파일이 없어 변조되지 않았습니다.")
        return False

    return outputApk

def modifyRes(startPath, outputApk):
    os.remove("{}{}META-INF\\MANIFEST.MF".format(startPath, os.sep))
    print("remove signInfo", "{}{}META-INF\\MANIFEST.MF".format(startPath, os.sep))
    for dirPath, dirs, files in os.walk(startPath):
        for f in files:
            fullPath = "{}{}{}".format(dirPath, os.sep, f)
            if "{}{}res{}".format(startPath, os.sep, os.sep) in fullPath:
                isModify = True
                with open(fullPath, "a") as modifyRes: 
                    modifyRes.write("\nappsuit modify so test!!")
                print("{} is modify".format(fullPath))
                return

def zipApk(folderInput, outputApk):
    with zipfile.ZipFile(outputApk, 'w') as zip:
        for dirPath, dirs, files in os.walk(folderInput):
            for file in files:
                if "{}\\{}".format(dirPath, file) == "META-INF\\MANIFEST.MF":
                    print("remove META-INF\\MANIFEST.MF")
                else: 
                    zip.write(os.path.join(dirPath, file), # 파일 이름
                        os.path.relpath(os.path.join(dirPath, file), folderInput), # 압축 파일의 이름(Default : 파일 이름과 같음)
                        compress_type = zipfile.ZIP_DEFLATED) # 압축 타입

def unZipApk(apkPath, outputPath):
    print("unzip {} to {}".format(apkPath, outputPath))
    execute_command("md {}".format(outputPath))
    with zipfile.ZipFile(apkPath, 'r') as zipIn:
        zipIn.extractall(outputPath)

def isDeviceConnected():
    result = execute_command("adb devices", 2)
    if "\tdevice" in result[1]: return True
    else: return False

def startRootTest(apkPath):
    print("startRootTest")

    if not isDeviceConnected():
        print("디바이스가 연결되지 않았습니다.");
        return

    execute_command("adb shell touch /sdcard/APPSUIT_ROOTING_TEST")
    print("done")

def endRootTest(apkPath):
    print("endRootTest")

    if not isDeviceConnected():
        print("디바이스가 연결되지 않았습니다.");
        return
    execute_command("adb shell rm -rf /sdcard/APPSUIT_ROOTING_TEST")
    print("done")


def resignApkWithZipalign(apkPath):
    print("resign", apkPath)
    apkPath = removeSignInfo(apkPath)
    outputApk = zipalign(apkPath)
    resign(outputApk)


def integrityApk(apkPath):
    print("start integrityApk")

    outputSoModApk = apkPath[:-4] + "_so_modify.apk"
    outputSoModDir = "modify_so"

    outputResModApk = apkPath[:-4] + "_res_modify.apk"
    outputResModDir = "modify_res"

    unZipApk(apkPath, outputResModDir)
    unZipApk(apkPath, outputSoModDir)
    
    modifyRes(outputResModDir, outputResModApk)
    isExist = modifySo(outputSoModDir, outputSoModApk)

    zipApk(outputResModDir, outputResModApk)
    if isExist: zipApk(outputSoModDir, outputSoModApk)

    zipalign(outputResModApk)
    if isExist: zipalign(outputSoModApk)

    resign(outputResModApk)
    if isExist: resign(outputSoModApk)

    shutil.rmtree(outputResModDir)
    shutil.rmtree(outputSoModDir)


def checkApkInfo(apkPath):
    print("apk 정보")
    isAppsuit = 0
    apkInfo = getApkInfo(apkPath)
    print(f"  package name        : {apkInfo['pkg']}")
    print(f"  versionName         : {apkInfo['verName']}")
    print(f"  versionCode         : {apkInfo['verCode']}")
    print(f"  launchable-activity : {apkInfo['lnchActv']}")
    
    with zipfile.ZipFile(apkPath, 'r') as zipIn:
        for f in zipIn.infolist():
            if "assets/appsuit/" in f.filename or "assets\\appsuit\\" in f.filename:
                isAppsuit = 1
            if "libAppSuit.so" in f.filename:
                isAppsuit = 2
                break

    if isAppsuit == 0: print("앱수트가 적용되지 않은 앱입니다.")
    else: print("앱수트 {}차 적용된 앱입니다.".format(isAppsuit))

def getApkInfo(apkPath):
    if len(re.compile('[^\u3131-\u3163\uac00-\ud7a3]+').sub('', apkPath)) >= 1:
        desApkPath = randomStrGenerator(20) + "_tmp.apk"
        os.rename(apkPath, desApkPath)
        result = execute_command("aapt dump badging \"{}\"".format(desApkPath), 2, change_path=True, src=apkPath, dst=desApkPath)
        os.rename(desApkPath, apkPath)
    
    else:
        result = execute_command("aapt dump badging \"{}\"".format(apkPath))

    apkInfo = {}
    for line in result:
        if "package: name="             in line: apkInfo["pkg"]      = line.split(' ')[1].replace("name=", '').replace("'", '')
        if "package: name="             in line: apkInfo["verName"]  = line.split(" ")[3].split("\\r")[0].replace("versionName=", "").replace("'", "")
        if "package: name"              in line: apkInfo["verCode"]  = line.split(" ")[2].replace("versionCode=", "").replace("'", "")
        if "launchable-activity: name=" in line: apkInfo["lnchActv"] = line.split(' ')[1].replace("name=", '').replace("'", '')
        if "Illegal byte sequence"      in line: return False

    return apkInfo


# def checkApkInfo(apkPath):
#     # print("apk 정보")
#     isAppsuit = 0
#     addb_data = [""]
#     with zipfile.ZipFile(apkPath, 'r') as zipIn:
#         for f in zipIn.infolist():
#             if "assets/appsuit/" in f.filename or "assets\\appsuit\\" in f.filename:
#                 isAppsuit = 1
#             if "libAppSuit.so" in f.filename:
#                 isAppsuit = 2
#                 break
#     if isAppsuit == 0: addb_data[0] = "앱수트가 적용되지 않은 앱입니다."
#     else: addb_data[0] = "앱수트 {}차 적용된 앱입니다.".format(isAppsuit)

#     result = execute_command("aapt dump badging \"{}\"".format(apkPath))
#     for line in result:
#         if "package: name="             in line: print("  package name        :", line.split(' ')[1].replace("name=", '').replace("'", ''))
#         if "package: name="             in line: print("  versionName         :", line.split(" ")[3].split("\\r")[0].replace("versionName=", "").replace("'", ""))
#         if "package: name"              in line: print("  versionCode         :", line.split(" ")[2].replace("versionCode=", "").replace("'", ""))
#         if "launchable-activity: name=" in line: print("  launchable-activity :", line.split(' ')[1].replace("name=", '').replace("'", ''))
#         if "Illegal byte sequence"      in line: print("앱 정보를 확인할 수 없습니다. 경로에 한글이 포함되어 있다면 삭제해주세요"); return

def removeApk(apkPath):
    result = execute_command("aapt dump badging \"{}\"".format(apkPath), 2)
    for line in result:
        if "package: name=" in line:
            packageName = line.split(' ')[1].replace("name=", '').replace("'", '')
            break
        if "Illegal byte sequence" in line: print("앱 정보를 확인할 수 없습니다. 경로에 한글이 포함되어 있다면 삭제해주세요"); return
    execute_command("adb uninstall \"{}\"".format(packageName))

def installApp(apkPath):
    return execute_command("adb install -r \"{}\"".format(apkPath))

def appStart(apkPath):
    # result = execute_command("aapt dump badging \"{}\"".format(apkPath), 2)
    # for line in result:
    #     if "package: name="             in line: packageName         = line.split(' ')[1].replace("name=", '').replace("'", '')
    #     if "launchable-activity: name=" in line: launchable_activity = line.split(' ')[1].replace("name=", '').replace("'", '')
    apkInfo = getApkInfo(apkPath)
    return execute_command(f"adb shell am start -n {apkInfo['pkg']}/{apkInfo['lnchActv']}")

def signingVerify(apkPath):
    result = execute_command("{} verify {}".format(apksignerPath, apkPath), 2)
    for line in result:
        if "ERROR" in line: 
            for line2 in result: print(line2)
            print("사이닝 되지 않은 apk입니다.")
            return False
    return True

def randomStrGenerator(str_len):
    random_string_form = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    random_string = "".join(random.choice(random_string_form) for x in range(str_len))
    return random_string
    


if "__main__" == __name__:
    appStart("C:\\Users\\lhsong\\Desktop\\sampleapp\\MyApplication3\\app\\release\\05191728\\myapp_release.apk")



