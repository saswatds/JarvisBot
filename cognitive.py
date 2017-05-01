import io
import os
import sys
import soundfile as sf
import json
from watson_developer_cloud import TextToSpeechV1

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

# import Google Cloud Library
from google.cloud import speech

json_file = os.path.join(os.path.dirname(__file__), 'resources', 'project-ion-jarvispi.json')
speech_client = speech.Client.from_service_account_json(json_file)

# TODO: Add this information to CREDS.py so that its obtained during installation
CLIENT_ACCESS_TOKEN = '9ebcb8b41a884ff88110fd7f2cb152e1'

SESSION_ID = 'edd25fbb-3658-4e0b-bbdc-c3c5611199e2'

ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

text_to_speech = TextToSpeechV1(
    username='fd7a1a11-bff2-4d9c-9900-946e7965b41c',
    password='rfnasZePfLDx',
    x_watson_learning_opt_out=True)  # Optional flag


def _transcribe():
    audio_path = os.path.join(os.path.dirname(__file__), 'audio/response.flac')

    data, samplerate = sf.read('recording.wav')
    sf.write(audio_path, data, samplerate)

    # Loads the audio into memory
    with io.open(audio_path, 'rb') as audio_file:
        content = audio_file.read()
        sample = speech_client.sample(content, encoding='FLAC')

    # Detects speech in the audio file
    result = sample.recognize('en-US')[0]

    if (result.confidence < 0.4):
        # Then play sound saying i didnt userstand what you said
        return None
    return result.transcript


def _understand(query="Hello"):
    request = ai.text_request()
    request.session_id = SESSION_ID
    request.query = query
    response = request.getresponse()
    # returns the json request
    return json.loads(response.read())


def _speak(sentence):
    response_path = os.path.join(os.path.dirname(__file__), 'audio/response.wav')
    with open(response_path,
              'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(sentence, accept='audio/wav',
                                      voice="en-US_MichaelVoice"))
        os.system('aplay -q {}'.format(response_path))


def doit():
    # the foolish text is a not understood text
    foolish_text = _transcribe()

    # if was not able to understand exit
    if foolish_text == None:
        return

    print "Foolish text: ", foolish_text
    # Send this to ai for understand
    ai_response = _understand(foolish_text)

    # Now get the fullfillment from the ai response
    speech_text = ai_response['result']['fulfillment']['speech']

    print "Response text: ", speech_text
    # Now speak the text response
    if speech_text != None or speech_text != '':
        _speak(speech_text)
