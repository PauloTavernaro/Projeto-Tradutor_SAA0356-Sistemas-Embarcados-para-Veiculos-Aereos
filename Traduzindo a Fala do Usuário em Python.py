import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from googletrans import Translator

#1st part of the code: dictionary
#_____________________________________________________________________________
#Here it is set the the languages and their labels
dic = ('afrikaans', 'af', 'albanian', 'sq', 
       'amharic', 'am', 'arabic', 'ar',
       'armenian', 'hy', 'azerbaijani', 'az', 
       'basque', 'eu', 'belarusian', 'be',
       'bengali', 'bn', 'bosnian', 'bs', 'bulgarian',
       'bg', 'catalan', 'ca', 'cebuano',
       'ceb', 'chichewa', 'ny', 'chinese (simplified)',
       'zh-cn', 'chinese',
       'zh-cn','chinese (traditional)',
       'zh-tw', 'corsican', 'co', 'croatian', 'hr',
       'czech', 'cs', 'danish', 'da', 'dutch',
       'nl', 'english', 'en', 'esperanto', 'eo', 
       'estonian', 'et', 'filipino', 'tl', 'finnish',
       'fi', 'french', 'fr', 'frisian', 'fy', 'galician',
       'gl', 'georgian', 'ka', 'german',
       'de', 'greek', 'el', 'gujarati', 'gu',
       'haitian creole', 'ht', 'hausa', 'ha',
       'hawaiian', 'haw', 'hebrew', 'he', 'hindi',
       'hi', 'hmong', 'hmn', 'hungarian',
       'hu', 'icelandic', 'is', 'igbo', 'ig', 'indonesian', 
       'id', 'irish', 'ga', 'italian',
       'it', 'japanese', 'ja', 'javanese', 'jw',
       'kannada', 'kn', 'kazakh', 'kk', 'khmer',
       'km', 'korean', 'ko', 'kurdish (kurmanji)', 
       'ku', 'kyrgyz', 'ky', 'lao', 'lo',
       'latin', 'la', 'latvian', 'lv', 'lithuanian',
       'lt', 'luxembourgish', 'lb',
       'macedonian', 'mk', 'malagasy', 'mg', 'malay',
       'ms', 'malayalam', 'ml', 'maltese',
       'mt', 'maori', 'mi', 'marathi', 'mr', 'mongolian',
       'mn', 'myanmar (burmese)', 'my',
       'nepali', 'ne', 'norwegian', 'no', 'odia', 'or',
       'pashto', 'ps', 'persian', 'fa',
       'polish', 'pl', 'portuguese', 'pt', 
       'punjabi', 'pa', 'romanian', 'ro', 'russian',
       'ru', 'samoan', 'sm', 'scots gaelic', 'gd',
       'serbian', 'sr', 'sesotho', 'st',
       'shona', 'sn', 'sindhi', 'sd', 'sinhala', 'si',
       'slovak', 'sk', 'slovenian', 'sl',
       'somali', 'so', 'spanish', 'es', 'sundanese',
       'su', 'swahili', 'sw', 'swedish',
       'sv', 'tajik', 'tg', 'tamil', 'ta', 'telugu',
       'te', 'thai', 'th', 'turkish',
       'tr', 'ukrainian', 'uk', 'urdu', 'ur', 'uyghur',
       'ug', 'uzbek',  'uz',
       'vietnamese', 'vi', 'welsh', 'cy', 'xhosa', 'xh',
       'yiddish', 'yi', 'yoruba',
       'yo', 'zulu', 'zu')
#_____________________________________________________________________________

#2nd part of the code: defining a function to take the language that the user wants to speak
#_____________________________________________________________________________
def language_speak():
     #Sets up the user microphone
     mic = sr.Microphone()
     recg = sr.Recognizer()
     #Using the microphone 
     with mic as source:
        #Controling the room noise
        recg.adjust_for_ambient_noise(source)
        #Setting a flag to tell the user to start talking
        print("Say in English the language you want to speak: ")
        #Storing what was said in the variable "audio"
        audio = recg.listen(source)

     #From this moment, the code will try to interpret the audio
     try:
        #Sending the audio to the algorithm to recognize voice patterns in English
        lang = recg.recognize_google(audio, language='en')
        #Then, the code shows what the user said
        print("Language you want to speak: " + lang)

     #If there is an error in catching the audio, the code awarns it
     except sr.Unknwon.Value.Error:
        print("I didn’t get it.")

     #It returns the transcription variable for future usage
     return lang
#_____________________________________________________________________________

#3rd part of the code: catching the language we want to speak and relating it to its label
#_____________________________________________________________________________
#Calling the function "language_speak()"
lang_speak = language_speak()

#Avoiding taking a word that is out of the dictionary
while (lang_speak.lower() not in dic):
    print("Language in which you are trying to speak\
    is currently not available. Please input some other language")
    print()
    lang_speak = language_speak()

#Storing the language label
lang_sp_label = dic[dic.index(lang_speak.lower())+1]
#_____________________________________________________________________________

#4th part of the code: defining a function to listen to the user 
#and to catch what the person says in the desired language. Also
#it calls the function
#_____________________________________________________________________________
def listening():
     #Sets up the user microphone
     mic = sr.Microphone()
     recg = sr.Recognizer()
     #Using the microphone 
     with mic as source:
        #Controling the room noise
        recg.adjust_for_ambient_noise(source)
        #Setting a flag to tell the user to start talking
        print("Say something: ")
        #Storing what was said in the variable "audio"
        audio = recg.listen(source)

     #From this moment, the code will try to interpret the audio
     try:
        #Sending the audio to the algorithm to recognize voice patterns in the desired language
        sentence = recg.recognize_google(audio, language=lang_sp_label)
        #Then, the code shows what the user said
        print("You said: " + sentence)

     #If there is an error in catching the audio, the code awarns it
     except sr.Unknwon.Value.Error:
        print("I didn’t get it.")

     #It returns the transcription variable for future usage
     return sentence

speech = listening()
#_____________________________________________________________________________

#5th part of the code: defining a function to take the language that the user
#wants for the translation
#_____________________________________________________________________________
def language_trans():
     #Sets up the user microphone
     mic = sr.Microphone()
     recg = sr.Recognizer()
     #Using the microphone 
     with mic as source:
        #Controling the room noise
        recg.adjust_for_ambient_noise(source)
        #Setting a flag to tell the user to start talking
        print("Say in English the language you want for the translation: ")
        #Storing what was said in the variable "audio"
        audio = recg.listen(source)

     #From this moment, the code will try to interpret the audio
     try:
        #Sending the audio to the algorithm to recognize voice patterns in English
        lang = recg.recognize_google(audio, language='en')
        #Then, the code shows what the user said
        print("Language you want for the translation: " + lang)

     #If there is an error in catching the audio, the code awarns it
     except sr.Unknwon.Value.Error:
        print("I didn’t get it.")

     #It returns the transcription variable for future usage
     return lang
#_____________________________________________________________________________

#6th part of the code: catching the language we want for the translation,
#and relating it to its label  
#_____________________________________________________________________________
#Calling the function "language_trans()"
lang_trans = language_trans()

#Avoiding taking a word that is out of the dictionary
while (lang_trans.lower() not in dic):
    print("Language in which you are trying to convert\
    is currently not available. Please input some other language")
    print()
    lang_trans = language_trans()

#Storing the language label
lang_tr_label = dic[dic.index(lang_trans.lower())+1]
#_____________________________________________________________________________

#7th part of the code: translating what the user written speech to the
#desired language 
#_____________________________________________________________________________
#Sending the function "Translator()" to the variable "translator"
translator = Translator()

# Translating the written speech
wr_speech = translator.translate(text = speech, dest = lang_tr_label)
#Taking only the "text" part (the translated written speech) from the 
#"translate" function
wr_speech = wr_speech.text
#_____________________________________________________________________________

#8th part of the code: defining a function to take the user's written speech 
#and play it in the desired language. Also
#it calls the function
#_____________________________________________________________________________
def speaking(written_speech):
    #Sending the written_speech file to Google Translate
    tts = gTTS(written_speech,lang=lang_tr_label)

    #Saving the audio file
    tts.save('hello.mp3')
    #Setting a flag to tell the user that the machine is going to speak
    print("I'm learning what you have said...")
    #Playing the audio
    playsound('hello.mp3')

#Playing the written speech through the function "speaking"
speaking(wr_speech)
#_____________________________________________________________________________