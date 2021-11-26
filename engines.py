from talon import speech_system, Context
from talon.engines.webspeech import WebSpeechEngine

webspeech = WebSpeechEngine()
speech_system.add_engine(webspeech)

# set the default engine
ctx = Context()
ctx.settings = {
    'speech.engine': 'wav2letter',
}