# Import Libraries
from googletrans import Translator
from gtts import gTTS
import speech_recognition as sr
import os
import googletrans
import pyaudio

# Create Recognizer Objects
recog1 = sr.Recognizer()
recog2 = sr.Recognizer()

# Create Microphone instance
# Device index is the microphone device plugged into the system, if 1 microphone is plugged in,
# then index is 0, if more than one, then have to determine mic plugged in
# device index is 2 since the microphone is number 2

mic = sr.Microphone(device_index=2)
# Using the microphone as source, we will capture voice and transform to text
with mic as source:
    # Speak start to start
    print("Say 'hello' in your language to start, or 'exit' to leave")
    print("---------------------------------------------------------")
    speak = gTTS("Say 'hello' in your language to start, or 'exit' to leave", slow=False)
    filename = "voice.mp3"
    speak.save(filename)
    os.system('mpg321 ' + filename)
    os.remove(filename)

    # Adjust for ambient noise
    recog1.adjust_for_ambient_noise(source, duration=0.2)
    # create an object to store the audio file
    audio = recog1.listen(source)
    

    try:
        voice_data = recog1.recognize_google(audio)
        translator = Translator()
        detected = translator.detect(voice_data).lang
        print(detected)
        print(voice_data)

        if 'exit' in voice_data:
            exit(1)

    except sr.UnknownValueError:
        print("Unable to understand the input")
    except sr.RequestError as e:
        print("Unable to provide required output".format(e))


def translate_to_other():
    # Listed for key word to start the program
    if 'hello' in voice_data:  # audio
        recog1 = sr.Recognizer()
        print("Choose your language to translate to")
        speak = gTTS("Choose your language to translate to", slow=False)
        filename = "voice.mp3"
        speak.save(filename)
        os.system('mpg321 ' + filename)
        os.remove(filename)

        lang = choose_langauge()
        with mic as source:
            # Adjust for ambient noise
            recog1.adjust_for_ambient_noise(source, duration=0.2)
            # create an object to store the audio file
            print('Speak a sentance')
            speak = gTTS("Speak a sentence", slow=False)
            filename = "voice.mp3"
            speak.save(filename)
            os.system('mpg321 ' + filename)
            os.remove(filename)

            recog1.adjust_for_ambient_noise(source, duration=0.2)
            # create audio
            audio = recog2.listen(source)
            get_phrase = recog2.recognize_google(audio)
            # Language detection
            translator = Translator()
            detect_lang = translator.detect(get_phrase).lang
            from_lang = detect_lang
            to_lang = lang
            try:
                get_phrase = recog2.recognize_google(audio)
                # make all letters lowercase in phrase for google translate
                get_phrase = get_phrase.lower()
                print('Translating: ' + get_phrase)
                # Using google translate
                text_to_translate = translator.translate(get_phrase, src=from_lang, dest=to_lang)
                # convert text to translate to a text to speech file
                speak = gTTS(text=text_to_translate.text, lang=to_lang, slow=False)
                # save the text to speech file to a voice file and convert to a string
                filename = "voice.mp3"
                speak.save(filename)
                os.system('mpg321 ' + filename)
                print("Translated Phrase from " + detect_lang + ": " + text_to_translate.text)
                os.remove(filename)

                if 'exit translator' in get_phrase:
                    exit(1)

            except sr.UnknownValueError:
                print("Unable to understand the input")
            except sr.RequestError as e:
                print("Unable to provide required output".format(e))
        translate_to_other()


def translate_to_english():
    translator = Translator()
    trans_detected = translator.translate(voice_data, src=detected, dest='en')
    trd = trans_detected.text
    print(trd)

    # Listed for key word to start the program
    if 'Hello' in trd:
        with mic as source:
            # Adjust for ambient noise
            recog1.adjust_for_ambient_noise(source, duration=0.2)

            #Get laugague to translate to
            #The Language takes the spoken input, detects destination language, and changes to the detected language
            get_language = translator.translate("Speak a sentance", src='en', dest=detected)
            print(get_language.text)

            speak = gTTS(get_language.text, slow=False)
            filename = "voice.mp3"
            speak.save(filename)
            os.system('mpg321 ' + filename)
            os.remove(filename)

            # create audio
            audio = recog2.listen(source)
            get_phrase = recog2.recognize_google(audio)

            # Language detection
            translator = Translator()
            detect_lang = translator.detect(get_phrase).lang
            from_lang = detect_lang
            to_lang = 'en'
            try:
                get_phrase = recog2.recognize_google(audio)
                # make all letters lowercase in phrase for google translate
                get_phrase = get_phrase.lower()
                # Translate
                print('Translating: ' + get_phrase)
                # Using google translate
                text_to_translate = translator.translate(get_phrase, src=from_lang, dest=to_lang)
                # convert text to translate to a text to speech file
                speak = gTTS(text=text_to_translate.text, lang=to_lang, slow=False)
                # save the text to speech file to a voice file and convert to a string
                filename = "voice.mp3"
                speak.save(filename)
                os.system('mpg321 ' + filename)
                print("Translated Phrase from " + detect_lang + ": " + text_to_translate.text)
                os.remove(filename)

                translate_to_english()

                # Exit translator
                if 'exit translator' in get_phrase:
                    exit(1)
                else:
                    print("******************")
            except sr.UnknownValueError:
                print("Unable to understand the input")
            except sr.RequestError as e:
                print("Unable to provide required output".format(e))

#Language choose that takes input spoken by the user, iterates through the Google Trans Dictionary,
# #and sets based on spoken selection
def choose_langauge():
    recog1 = sr.Recognizer()
    languages = googletrans.LANGUAGES
    #Changing Dictionary to List to iterate thorugh easier than a non-editable dictionary
    vals = list(languages.values())
    keys = list(languages.keys())
    for lang_detect in languages:
        with mic as source:
            audio = recog1.listen(source)
            try:
                lang_detect = recog1.recognize_google(audio)
                lang_detect = lang_detect.lower()
                spoken = keys[vals.index(lang_detect)]
                print(spoken)
                return spoken
            except sr.UnknownValueError:
                print("Unable to understand the input")
            except sr.RequestError as e:
                print("Unable to provide required output".format(e))


if 'en' in detected:
    translate_to_other()
else:
    translate_to_english()



