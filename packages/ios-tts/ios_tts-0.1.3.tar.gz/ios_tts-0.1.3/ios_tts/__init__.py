import time
from unitts.basedriver import BaseDriver
from unitts.voice import Voice
from pyobjus import autoclass, protocol, objc_str
from pyobjus.dylib_manager import load_framework, INCLUDE
load_framework(INCLUDE.AVFoundation)
load_framework('/System/Library/Frameworks/Foundation.framework')
NSTimer = autoclass('NSTimer')
NSString = autoclass('NSString')
NSArray = autoclass('NSArray')
NSObject = autoclass('NSObject')
AVSpeechSynthesizer = autoclass('AVSpeechSynthesizer')
AVSpeechUtterance = autoclass('AVSpeechUtterance')
AVSpeechSynthesisVoice = autoclass('AVSpeechSynthesisVoice')
NSURL = autoclass('NSURL')

from text2sentences import text_to_sentences
from .version import __version__

def language_by_lang(lang):
	locales = {
		'zh':'zh-CN',
		'en':'en-US',
		'tr':'tr-TR',
		'th':'th-TH',
		'sv':'sv-SE',
		'es':'es-ES',
		'sk':'sk-SK',
		'ru':'ru-RU',
		'ro':'ro-RO',
		'pt':'pt-PT',
		'pl':'pl-PL',
		'no':'no-NO',
		'ko':'ko-KO',
		'ja':'ja-JP',
		'it':'it-IT',
		'id':'id-ID',
		'hu':'hu-HU',
		'hi':'hi-IN',
		'el':'el-GR',
		'de':'de-DE',
		'fr':'fr-FR',
		'nl':'nl-NL',
		'da':'da-DK',
		'cs':'cs-CZ',
		'ar':'ar-SA'
	}
	return locales.get(lang, None)

def buildDriver(proxy, **kw):
	print(f'ios_tts version {__version__}')
	return IOSSpeechDriver(proxy, **kw)

class IOSSpeechDriver(BaseDriver):
	def __init__(self, proxy, **kw):
		super().__init__(proxy)
		self._tts = AVSpeechSynthesizer.alloc().init()
		# self._tts.delegate = self
		self.volume = 1
		self._completed = True
		self.rate = 180
		self.set_stop_period()
		self.voice = None
		print(f'IOSTTS driver version {__version__}')
		self.speaking_sentence = None
		self.get_voices()

	def set_voice(self, lang):
		pass

	def get_voice_by_lang(self, lang):
		for v in self.voices:
			x = map(lambda x:lang==x[:len(lang)], v.languages)
			if True in x:
				default_language = language_by_lang(lang)
				if default_voice is None:
					return v.id
				if default_language in v.languages:
					return v.id
		raise Exception(f'{lang} is not supported language')
			
	def _toVoice(self, voice):
		id = voice.valueForKey_('identifier')
		v = Voice(id)
		v.name = voice.valueForKey_('name')
		v.gender = voice.valueForKey_('gender')
		v.languages = [voice.valueForKey_('language')]
		return v

	def get_voices(self):
		voices = AVSpeechSynthesisVoice.speechVoices()
		x = [ self._toVoice(v) for v in \
					[voices.objectAtIndex_(i) \
							for i in range(voices.count()) ] ]
		self.voices = x
		return x
		
	def isSpeaking(self):
		return self._tts.isSpeaking()

	def destroy(self):
		self._tts.delegate = None
		del self._tts
		self._tts = None
		
	def pre_command(self, sentence):
		return sentence.start_pos, sentence
		
	def command(self, pos, sentence):
		print('command()', sentence.text)
		self.speak_sentence(sentence)

	def set_stop_period(self):
		r = 1.0 / float(self.rate)
		self.semi_stop_period = 1.5 * r
		self.sentence_stop_period = 3.0 * r

	def pauseplay(self):
		self._tts.pauseSpeakingAtBoundary()

	def continueplay(self):
		self._tts.continueSpeaking()

	def stop(self):
		if self._proxy.isBusy():
			self._completed = False
		self._tts.stopSpeakingAtBoundary()

	def nss2s(self, nsobj):
		x = nsobj.UTF8String()
		if isinstance(x, str):
			return x
		return x.decode('utf-8')

	def set_utterances_by_sentence(self, utterance, sentence):
		if sentence.dialog:
			utterance.pitchMultiplier = 1.25
		else:
			utterance.pitchMultiplier = 1.0
		locale = language_by_lang(sentence.lang)
		voice = AVSpeechSynthesisVoice.voiceWithLanguage_(objc_str(locale))
		utterance.voice = voice
		# utterance.rate = self.rate

	def speak_sentence(self, sentence):
		utterance = AVSpeechUtterance.speechUtteranceWithString_(objc_str(sentence.text))
		self.set_utterances_by_sentence(utterance, sentence)
		r = self._tts.speakUtterance_(utterance)
		print('speakUtterance() =', r)
		print('speak_sentence() finished')

	def getProperty(self, name):
		if name == 'voices':
			return self.voices
		elif name == 'voice':
			return self.voice
		elif name == 'rate':
			return None
		elif name == 'volume':
			return None
		elif name == "pitch":
			print("Pitch adjustment not supported when using NSSS")
		else:
			raise KeyError('unknown property %s' % name)

	def setProperty(self, name, value):
		return
		if name == 'voice':
			# vol/rate gets reset, so store and restore it
			self.voice = value
		elif name == 'rate':
			self._tts.setRate_(value)
		elif name == 'volume':
			self._tts.setVolume_(value)
		elif name == 'pitch':
			print("Pitch adjustment not supported when using NSSS")
		else:
			raise KeyError('unknown property %s' % name)

	def save_to_file(self, text, filename):
		url = NSURL.fileURLWithPath_(filename)
		self._tts.startSpeakingString_toURL_(text, url)

	"""
	@protocol('AVSpeechSynthesizerDelegate')
	def speechSynthesizer_didStart_(self, *args):
		print('didStart_(): args=', args)
		return

	@protocol('AVSpeechSynthesizerDelegate')
	def speechSynthesizer_didCancel_(self, *args):
		print('didCancel_(): args=', args)
		return

	@protocol('AVSpeechSynthesizerDelegate')
	def speechSynthesizer_didContinue_(self, *args):
		print('didContinue_(): args=', args)
		return

	@protocol('AVSpeechSynthesizerDelegate')
	def speechSynthesizer_didPause_(self, *args):
		print('didPause_(): args=', args)
		return

	@protocol('AVSpeechSynthesizerDelegate')
	def speechSynthesizer_didFinish_(self, *args):
		print('didFinish_(): args=', args)
		if self.speaking_sentence.semi_sentenece:
			time.sleep(self.simi_stop_period)
		else:
			time.sleep(self.sentence_stop_period)
		self.speak_next_utterance()
		return

	@protocol('AVSpeechSynthesizerDelegate')
	def speechSynthesizer_willSpeakRangeOfSpeech_utterance_(self, *args):
		print('willSpeakRangeOfSpeech_(): args=', args)
	"""

