from dotenv import load_dotenv

from appium import webdriver

from appium.webdriver.common.touch_action import TouchAction
from appium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

import os
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import time
import argparse

import telnetlib

load_dotenv()

class Device:
    def __init__(self,avd,device_name,duration,unit_of_time,use_duration,proxy,longitude, latitude):
        self.platform = os.environ["PLATFORM_NAME"]
        self.wait_time = os.environ["WAIT_TIME"]
        self.emulator_dir = os.environ["EMULATOR_DIR"]
        self.adb_dir = os.environ["ADB_DIR"]
        self.device_name = device_name
        self.avd = avd
        self.duration = duration
        self.unit_of_time = unit_of_time
        self.use_duration = use_duration
        self.proxy = proxy
        self.longitude = longitude
        self.latitude = latitude
        print("\n\n")
        print(f"PLATFORM: {self.platform}")
        print(f"DEVICE NAME: {self.device_name}")
        print(f"AVD: {self.avd}")
        print(f"WAIT TIME: {self.wait_time}")
        print(f"EMULATOR DIRECTORY: {self.emulator_dir}")
        print(f"ADB DIRECTORY: {self.adb_dir}")
        print(f"DURATION: {self.duration}")
        print(f"UNIT OF TIME: {self.unit_of_time}")
        print(f"USE DURATION: {self.use_duration}")
        print(f"LONGITUDE: {self.longitude}")
        print(f"LATITUDE: {self.latitude}")
    
    def setup(self):
        desired_caps = {
            "platformName": self.platform,
            "deviceName": self.device_name,
            "avd": self.avd,
            "isHeadless": True,

        } 

        webdriver_url = os.environ["WEBDRIVER_URL"]
        print("WEBDRIVER URL: ", webdriver_url)
        # self.driver = webdriver.Remote(webdriver_url, desired_caps,strict_ssl=False)
        self.driver = webdriver.Remote(webdriver_url, desired_caps)
        print("SELF DRIVER: ",self.driver,"\n\n")
        self.actions  = TouchAction(self.driver)
        self.driver.set_location(self.latitude,self.longitude, 100.0)
        tn = telnetlib.Telnet("127.0.0.1", self.device_name.split("-")[1], 10)
        tn.set_debuglevel(9)
        tn.read_until(bytes("OK", 'utf-8'),5)
        tn.write(bytes(f"geo fix {self.longitude} {self.latitude}\n", 'utf-8'))
        tn.write(bytes("exit\n",'utf-8'))
        print(tn.read_all)

    def tearDown(self):
        self.driver.quit()

    def home_button(self):
        self.driver.press_keycode(3)
        time.sleep(1)

    def restart_adb_server(self):
        os.chdir(self.adb_dir)
        kill_server = subprocess.Popen(['./adb','kill-server'])
        kill_server.wait()
        start_server = subprocess.Popen(['./adb','start-server'])
        start_server.wait()
        devices = subprocess.check_output(['./adb','devices'])
        print(f'adb devices: {devices}')

    def stop_emulator(self):
        os.chdir(self.adb_dir)
        kill_emu = subprocess.Popen(['./adb','-s',self.device_name,'emu','kill'])
        kill_emu.wait()
        print('stopped emulator\n')

    def cold_boot(self):
        os.chdir(self.adb_dir)
        kill_emu = subprocess.Popen(['./adb','-s',self.device_name,'emu','kill'])
        kill_emu.wait()
        print('killed the emulator\n')
        time.sleep(30)
        os.chdir(self.emulator_dir)
        cold_boot = subprocess.Popen(f'./emulator -avd {self.avd} -writable-system -no-window -http-proxy http://127.0.0.1:{self.proxy} -no-passive-gps &', shell=True)
    
    def online(self):
        os.chdir(self.adb_dir)
        online = subprocess.check_output(['./adb', 'devices'])
        for split in str(online).split('\\n'):
            if split.startswith(self.device_name):
                print('device is online')
                return True
        return False

    def get_coord_from_bounds(self, bounds):
        box = [int(s) for s in bounds.replace('[',',').replace(']',',').split(',') if s.isdigit()]
        x = (box[0] + box[2])//2
        y = (box[1] + box[3])//2
        return {'x':x,'y':y}

    def refresh(self):
            self.actions.long_press(None,540,420).move_to(None,540,1080).release().perform()

    def open_whisper_nearby(self):
        chain = ActionChains(self.driver)
        chain.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        chain.w3c_actions.pointer_action.move_to_location(540, 1600)
        chain.w3c_actions.pointer_action.pointer_down()
        chain.w3c_actions.pointer_action.move_to_location(540, 430)
        chain.w3c_actions.pointer_action.release()
        chain.perform()
        
        time.sleep(15)

        root = self.get_root()
        iteration = root.find('''.//android.widget.TextView[@content-desc="Whisper"]''')
        bounds = self.get_coord_from_bounds(iteration.get('bounds'))
        self.actions.tap(None,bounds['x'],bounds['y']).perform()
        self.actions.wait(ms=self.wait_time).perform()
        try:
            for attempt in range(5):
                print(attempt)
                try:
                    nearby = self.actions.tap(None,675,207).perform()
                    time.sleep(5)
                except Exception as e:
                    print("\nFailed to tap on Nearby tab.\n")
                    time.sleep(5)
                else:
                    if nearby != None:
                        break
                    raise ValueError("nearby should not be None.\n")
        except Exception as e:
            print("\nFailed attempt loop to open Nearby tab.\n")
        else:
            if nearby == None:
                print("\nFailed to open Whisper Nearby.\n")

    def get_root(self):
        page_source = self.driver.page_source
        tree = ET.ElementTree(ET.fromstring(page_source))
        root = tree.getroot()
        return root

    def get_coord_from_bounds(self, bounds):
        box = [int(s) for s in bounds.replace('[',',').replace(']',',').split(',') if s.isdigit()]
        x = (box[0] + box[2])//2
        y = (box[1] + box[3])//2
        return {'x':x,'y':y}

    def undo_freeze(self):
        for i in range(2):
            self.actions.long_press(None,540,400).move_to(None,540,1700).release().perform()
            time.sleep(2)
    
    def detected_freeze(self):
        if len(os.listdir(self.output_dir)) == self.num_batches:
            return True
        return False

    def scroll(self):
        if self.use_duration:
            delta = timedelta(minutes=0)
            if self.unit_of_time == 'minutes':
                delta = timedelta(minutes=int(self.duration))
            elif self.unit_of_time == 'hours':
                delta = timedelta(hours=int(self.duration))
            elif self.unit_of_time == 'seconds':
                delta = timedelta(seconds=int(self.duration))
            later = datetime.now() + delta

            while (datetime.now() < later):
                try:
                    self.actions.long_press(None,540,1700).move_to(None,540,300).release().perform()
                    time.sleep(2)
                except Exception as e:
                    print("\nException\n",e)
        else:
            while True:
                try:
                    self.actions.long_press(None,540,1700).move_to(None,540,300).release().perform()
                    time.sleep(2)
                except Exception as e:
                    print("\nException\n",e)

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Perform mobile app scrape")

    duration = parser.add_argument("-d","--Duration",type=int,help="duration of time to collect whispers for",required=True)
    use_duration = parser.add_argument("-use", "--UseDuration",type=str,help="to use duration or not",required=True)
    unit_of_time = parser.add_argument("-u","--UnitOfTime",type=str,help="unit of time for specified duration",required=True)
    avd = parser.add_argument("-avd", "--AVD", help="AVD Name",required=True)
    device = parser.add_argument("-device", "--DeviceName", help="Device Name",required=True)
    proxy = parser.add_argument("-p","--Proxy", help="Http Proxy",required=True)
    longitude = parser.add_argument("-long","--Longitude", help="Set Longitude")
    latitude = parser.add_argument("-lat","--Latitude", help="Set Latitude")

    args = parser.parse_args()

    device = Device(args.AVD,args.DeviceName,args.Duration,args.UnitOfTime,args.UseDuration,args.Proxy,args.Longitude,args.Latitude)

    failed = False
    device.restart_adb_server()
    time.sleep(10)
    
    device.setup()
    device.cold_boot()

    for i in range(5):
        print('re-setting up attempt: ', i)
        try:
            device.setup()
        except Exception as e:
            print(e)
        else:
            break
        if i == 4:
            failed = True
        time.sleep(10)

    if failed == True:
        raise ValueError('Re-setting up failed all attempts.')

    time.sleep(30)

    for i in range(5):
        print('opening app attempt: ',i)
        try:
            device.open_whisper_nearby()
        except Exception as e:
            print(e)
        else:
            break
        time.sleep(10)
        if i == 4:
            failed = True

    if failed == True:
        raise ValueError('Opening app failed all attempts.')

    time.sleep(10)

    for i in range(5):
        print('refreshing attempt: ', i)
        try:
            device.refresh()
        except Exception as e:
            print(e)
        else:
            break
        time.sleep(10)
        if i == 4:
            failed = True

    if failed == True:
        raise ValueError('Refreshing failed all attempts.')

    for i in range(5):
        print('scrolling attempt: ', i)
        try:
            device.scroll()
            print("scrolling...")
        except Exception as e:
            print(e)
        else:
            break
        time.sleep(10)
        if i == 4:
            failed = True
    
    if failed == True:
        raise ValueError('Scrolling failed all attempts.')

    device.tearDown()
    device.stop_emulator()
    

# appium --address 127.0.0.1 -p 4723 --session-override
# python3 automate_mitm.py -d {duration} -u {unit of time} -use {whether to use a duration or while True} -avd {avd name} -device {emulator and number}