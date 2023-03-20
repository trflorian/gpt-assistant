import os
import openai

import azure.cognitiveservices.speech as speechsdk


def recognize_from_microphone():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'),
                                           region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_recognition_language = "de-CH"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")


def text_to_speech(text):
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'),
                                           region=os.environ.get('SPEECH_REGION'))
    # Note: the voice setting will not overwrite the voice element in input SSML.
    speech_config.speech_synthesis_voice_name = "de-CH-LeniNeural"

    # use the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    result = speech_synthesizer.speak_text_async(text).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))


def setup_opeanai():
    openai.organization = "org-NxrmkQD0vuaMOkyXICvK1vh9"
    openai.api_key = os.getenv("OPENAI_API_KEY")


def get_chat_response(user_request, system_text, chat_history=[]):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_text},
            *chat_history,
            {"role": "user", "content": user_request},
        ],
        max_tokens=200
    )
    return response['choices'][0]['message']['content']


def main():
    setup_opeanai()

    # prompt_fn = 'system_text_request_type_german.txt'
    prompt_fn = 'chat_bot.txt'

    with open(f'prompts/{prompt_fn}') as f:
        system_text = '\n'.join(f.readlines())

    chat_history = []

    while True:
        request_text = recognize_from_microphone()

        response = get_chat_response(request_text, system_text, chat_history)

        chat_history.append({
            "role": "user",
            "content": request_text
        })
        chat_history.append({
            "role": "assistant",
            "content": response
        })

        print(response)

        text_to_speech(response)


if __name__ == '__main__':
    main()
