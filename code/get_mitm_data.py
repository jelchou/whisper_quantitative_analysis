import os
import json
from pprint import pprint
import requests 
import pandas as pd
import argparse
from dotenv import load_dotenv

load_dotenv()

dump = os.environ["DUMP_DIR"]
text = os.environ["TEXT_DIR"]
images = os.environ["IMAGES_DIR"]

def batch_to_csv_and_imgs(avd):
    count = 0
    curr_pd = None
    directory = os.path.join(dump,avd)
    for filename in os.listdir(directory):
        with open(os.path.join(directory,filename), 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('{"scroll_id"'):
                    mitm_data = json.loads(line)
                    whispers = mitm_data['whispers']
                    print(f"This batch contains {len(whispers)} whisper texts")
                    count += len(whispers)
                    for whisper in whispers:
                        # get images
                        whisper['avd'] = os.environ["AVD"] 
                        whisper['text'] = whisper['text'].replace('\n',' ')
                        wid = whisper['wid']
                        image_url = whisper['url']
                        img_data = requests.get(image_url).content
                        if not os.path.exists(os.path.join(images,avd)):
                            os.makedirs(os.path.join(images,avd))
                        with open(os.path.join(images,avd,f'{wid}.jpg'), 'wb') as handler:
                            handler.write(img_data)
                        # save mitmdump output to csv
                        df = pd.json_normalize(whisper)
                        curr_pd = pd.concat([curr_pd,df])
    print(f"Total Whispers Collected: {count}")
    return curr_pd

def to_csv(df,avd):
    csvFile = df.to_csv(os.path.join(text,f'{avd}.csv'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieving & Storing Text/Images From Collected Batches of Whisper Posts")
    device = parser.add_argument("-avd", "--AVD", help="AVD Name",required=True)
    args = parser.parse_args()

    df = batch_to_csv_and_imgs(args.AVD)
    to_csv(df,args.AVD)