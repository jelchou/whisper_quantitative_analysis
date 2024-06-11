import time
import schedule 
import subprocess

avd_args = [
    {'avd':'nyc_young', 'proxy':8081, 'longitude':-73.9903, 'latitude':40.7301},
    {'avd':'nyc_old', 'proxy':8082, 'longitude':-73.9903, 'latitude':40.7301},
    {'avd':'la_young', 'proxy':8083, 'longitude':-118.2705, 'latitude':34.0226},
    {'avd':'la_old', 'proxy':8084, 'longitude':-118.2705, 'latitude':34.0226},
    {'avd':'chicago_young', 'proxy':8085, 'longitude':-87.6638, 'latitude':41.8781},
    {'avd':'chicago_old', 'proxy':8086, 'longitude':-87.6638, 'latitude':41.8781},
]

def run_avds():
    duration='60' 
    unit_of_time='minutes'
    use_duration='True'
    device='emulator-5554'

    current_avd = avd_args.pop(0)
    avd_args.append(current_avd)

    avd = current_avd['avd']
    proxy = current_avd['proxy']
    longitude = current_avd['longitude']
    latitude = current_avd['latitude']

    run = subprocess.Popen(f'python3 automate_mitm.py -d {duration} -u {unit_of_time} -use {use_duration} -avd {avd} -device {device} -p {proxy} -long {longitude} -lat {latitude}', shell=True)

if __name__ == "__main__":
    # SCHEDULE
    schedule.every(70).minutes.do(run_avds)
    schedule.run_all()

    while True:
        schedule.run_pending()
        time.sleep(1)
