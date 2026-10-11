import os

def client(api_key=None):
	# imported here so that importing Services does not require the elevenlabs package
	from elevenlabs import ElevenLabs
	from elevenlabs.environment import ElevenLabsEnvironment
	if api_key is None:
		api_key = os.environ.get('ELEVENLABS_API_KEY')
	if not api_key:
		raise RuntimeError('No ElevenLabs API key: pass api_key or set ELEVENLABS_API_KEY')
	return ElevenLabs(api_key=api_key, environment=ElevenLabsEnvironment.PRODUCTION)

def save(result, output_path):
	import elevenlabs
	elevenlabs.save(result, output_path)

def text_to_speech(text, voice_id, output_path, api_key=None):
	result = client(api_key).text_to_speech.convert(
		text=text,
		voice_id=voice_id,
		model_id="eleven_v3",
		language_code="he",
		output_format="mp3_44100_128",
	)
	save(result, output_path)
	return True

def speech_to_speech(input_path, voice_id, output_path, api_key=None):
	with open(input_path, 'rb') as f:
		audio_data = f.read()
	result = client(api_key).speech_to_speech.convert(
		voice_id=voice_id,
		output_format="mp3_44100_128",
		model_id="eleven_multilingual_sts_v2",
		audio=audio_data
	)
	save(result, output_path)
	return True

def forced_alignment(audiofile, text, api_key=None):
	with open(audiofile, 'rb') as audio_file:
		response = client(api_key).forced_alignment.create(
			file=audio_file,
			text=text
		)
	return response

def word_alignment(audiofile, text, api_key=None):
	response = forced_alignment(audiofile, text, api_key)
	word_tuples = []
	for word in response.words:
		if word.text.strip():
			word_tuples.append((word.start, word.end, word.text))
	return word_tuples
