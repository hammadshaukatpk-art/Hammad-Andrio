import os, subprocess, shutil, re
from pathlib import Path
SDK=Path(os.environ.get("ANDROID_HOME",str(Path.home()/"AppData/Local/Android/Sdk")))
def tool(name):
    suffix=".bat" if os.name=="nt" and name in ("avdmanager","sdkmanager") else ".exe" if os.name=="nt" else ""
    folder={"emulator":"emulator","adb":"platform-tools","avdmanager":"cmdline-tools/latest/bin","sdkmanager":"cmdline-tools/latest/bin"}[name]
    p=SDK/folder/(name+suffix)
    return str(p) if p.exists() else shutil.which(name)
def call(name,*args,timeout=120,input=None):
    exe=tool(name)
    if not exe: raise RuntimeError("Android SDK component missing: "+name+". Install Android Studio SDK tools.")
    p=subprocess.run([exe,*map(str,args)],input=input,text=True,capture_output=True,timeout=timeout)
    if p.returncode: raise RuntimeError((p.stderr or p.stdout)[-1500:])
    return p.stdout.strip()
def devices():
    return [x.strip() for x in call("emulator","-list-avds").splitlines() if x.strip()]
def images():
    return [x.split("|")[0].strip() for x in call("sdkmanager","--list_installed").splitlines() if x.strip().startswith("system-images;")]
def create(name,image,ram,cores):
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]{0,59}",name): raise ValueError("Invalid device name")
    if image not in images(): raise ValueError("System image not installed")
    if not 512<=ram<=16384 or not 1<=cores<=16: raise ValueError("Invalid resources")
    call("avdmanager","create","avd","-n",name,"-k",image,"--device","pixel",input="no\n")
    p=Path.home()/".android"/"avd"/(name+".avd")/"config.ini"
    if p.exists():
        data=[s for s in p.read_text(errors="replace").splitlines() if not s.startswith(("hw.ramSize=","hw.cpu.ncore="))]
        p.write_text("\n".join(data+[f"hw.ramSize={ram}",f"hw.cpu.ncore={cores}"])+"\n")
def running():
    result={}
    for line in call("adb","devices").splitlines():
        if line.startswith("emulator-") and "\tdevice" in line:
            serial=line.split()[0]
            try: result[call("adb","-s",serial,"emu","avd","name").splitlines()[0]]=serial
            except Exception: pass
    return result
def start(name):
    if name not in devices(): raise ValueError("Unknown instance")
    if name in running(): raise ValueError("Already running")
    subprocess.Popen([tool("emulator"),"-avd",name,"-no-snapshot-save"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def stop(name):
    serial=running().get(name)
    if not serial: raise ValueError("Device not running")
    call("adb","-s",serial,"emu","kill")
def delete(name):
    if name in running(): raise ValueError("Stop device before deleting")
    call("avdmanager","delete","avd","-n",name)
def install(name,apk):
    serial=running().get(name)
    if not serial: raise ValueError("Device not running")
    if not Path(apk).is_file() or Path(apk).suffix.lower()!=".apk": raise ValueError("Invalid APK")
    return call("adb","-s",serial,"install","-r",apk,timeout=240)
