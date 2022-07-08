import asyncio
import subprocess

from gtts import gTTS
import re

from tgvoip import VoIPServerConfig
from tgvoip_pyrogram import VoIPFileStreamService
import pyrogram

import uuid

API_HASH = 'Your_API Hash'
API_ID = 0 # API ID
CLIENT_NAME = 'Rose'

VoIPServerConfig.set_bitrate_config(80000, 100000, 60000, 5000, 5000)
client = pyrogram.Client(CLIENT_NAME, API_ID, API_HASH)
voip_service = VoIPFileStreamService(client, receive_calls=False)  # use VoIPNativeIOService for native I/O

# Converts text to an audio file
def text_to_mp3(text: str, lang: str, location: str):
    text_to_speech = gTTS(text=text, lang=lang, slow=False)
    text_to_speech.save(location)


def get_mp3_length(location: str) -> float:
    args = ("ffprobe", "-show_entries", "format=duration", "-i", location)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    r = re.findall(r'(?<=duration=)(.*)(?=\\n\[/F)', str(output))
    return float(r[0])


def mp3_to_binary(source: str, destination: str = ''):
    if not destination:
        destination = f'./binary_audio/{uuid.uuid4()}.raw'
    args = ('ffmpeg', '-i', source, '-f', 's16le', '-ac', '1', '-ar', '48000', '-acodec', 'pcm_s16le', destination)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    return destination


async def main(text='Hello world', lang='en', times=1, user=''):
    async with client:
        location = './audio/test.mp3'
        text_to_mp3(text=text, lang=lang, location=location)
        duration = get_mp3_length(location=location)
        binary_audio_location = mp3_to_binary(source=location)
        call = await voip_service.start_call(user)
        for i in range(times):
            call.play(binary_audio_location)
        call_has_ended = False

        @call.on_call_state_changed
        def state_changed(call, state):
            print('State changed:', state)

        # you can use `call.on_call_ended(lambda _: app.stop())` here instead
        @call.on_call_ended
        async def call_ended(call):
            global call_has_ended
            call_has_ended = True

        while True:
            await asyncio.sleep(1)
            try:
                if call.ctrl.call_duration > duration * times or call_has_ended:
                    await call.discard_call()
                    break
            except:
                break
        await client.stop()


loop = asyncio.get_event_loop()
loop.run_until_complete(main(
    text='text',
    times=2, user='@username'))
