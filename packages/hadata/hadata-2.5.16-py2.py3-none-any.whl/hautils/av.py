import os
import subprocess

from hautils.logger import logger

DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
YOUR_API_URL = 'https://api.deepgram.com/v1'

def video_to_audio(file_name):
    audio_file = "%s.wav" % (file_name,)
    command = 'ffmpeg -y -i %s -ab 160k -ar 44100 -vn %s' % (file_name, audio_file,)
    subprocess.call(command, shell=True)
    return audio_file


async def extract_transcript(file_name):
    logger.info("config %s - %s" % (DEEPGRAM_API_KEY, YOUR_API_URL))
    logger.info("calling extract transcript on %s" % (file_name,))
    dg_client = Deepgram({'api_key': DEEPGRAM_API_KEY, 'api_url': YOUR_API_URL})
    source = {'buffer': open(file_name, 'rb').read(), 'mimetype': 'audio/wav'}
    response = await dg_client.transcription.prerecorded(source, {'punctuate': False, })
    logger.debug(response)
    return response['results']['channels'][0]['alternatives'][0]['transcript']


