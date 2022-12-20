#Defining the libraries from Qt
from PySide2.QtCore import Qt, QObject, QThread
from PySide2.QtCore import Signal
from PySide2.QtGui import QFont, QColor
from PySide2.QtWidgets import (
    QApplication, QLabel, QPushButton, QWidget, QVBoxLayout, QMainWindow
)

#Defining the libraries for the translating function itself
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from googletrans import Translator
from subprocess import check_output
import time


#Setting a class to group the functions responsible for catching the language for the speech
class Language_Speak (QObject):

    #Setting the signals to link this class to the Window one in order to show on the screen
    #the labels set in the later class mentioned
    finished = Signal()
    sec_screen_interface = Signal()
    lang_not_in_dic = Signal()
    lang_in_dic = Signal()
    only_lang = Signal(str)
    show_lang_in_dic = Signal()
    didnt_get = Signal()
    language = Signal(str)


    #Starts the function to catch the language for the speech
    def speak(self):

        #Setting a list of languages
        self.dic = ('afrikaans', 'af', 'albanian', 'sq', 
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

        #Sets up the user microphone
        mic = sr.Microphone()
        recg = sr.Recognizer() 
        
        #The code enters in a while loop until it gets the language
        while True:
            #Using the microphone
            with mic as source:
                #Controling the room noise
                recg.adjust_for_ambient_noise(source)
                #Setting a flag to tell the user to start talking
                self.sec_screen_interface.emit()
                #Storing what was said in the variable "audio"
                audio = recg.listen(source)

        #From this moment, the code will try to interpret the audio

            try:
                #Sending the audio to the algorithm to recognize voice patterns in English
                lang = recg.recognize_google(audio, language='en')
                
                #Then, if the language said doesn't match with any of the options in the dictionary, 
                #the user will know it, and will be asked to say it again.
                if (lang.lower() not in self.dic):
                    self.lang_not_in_dic.emit()
                    time.sleep(3)
                    continue
                #On the other hand, if the language matches with some of the options in the dictionary, 
                #the code breaks the loop and tell the user the language chosen
                elif (lang.lower() in self.dic):
                    (self.lang_in_dic.emit()) + (self.only_lang.emit(lang))
                    self.show_lang_in_dic.emit()
                    break
            #If there is an error in catching the audio, the code awarns it
            except:
                self.didnt_get.emit()
                time.sleep(2)
                continue

        #Storing the language label
        self.lang_speak = self.dic[self.dic.index(lang.lower())+1]

        #Returns the language label
        return self.lang_speak
    
    #This function just takes the result of the "speak" function to be used in the "Listening" class
    def send_lang_label(self):
        self.language.emit(self.lang_speak)


#Setting a class to place the fuction to catch what the user says
class Listening(QObject):

    #Setting the signals to link this class to the Window one in order to show on the screen
    #the labels set in the later class mentioned
    finished = Signal()
    say_something = Signal()
    you_said = Signal()
    sentence = Signal(str)
    didnt_get = Signal()

    def listen(self, language):
        #Takes the result of the function "send_lang_label" in order to set the language for recognition
        #Sets up the user microphone
        mic = sr.Microphone()
        recg = sr.Recognizer()
        #The code enters in a while loop until it gets what the user said
        while True:
            #Using the microphone 
            with mic as source:
                #Controling the room noise
                recg.adjust_for_ambient_noise(source)
                #Setting a flag to tell the user to start talking
                self.say_something.emit()

                #Storing what was said in the variable "audio"
                audio = recg.listen(source)

            #From this moment, the code will try to interpret the audio
            try:
            #Sending the audio to the algorithm to recognize voice patterns in the desired language
                self.sentence_said = recg.recognize_google(audio, language=language)
                #Then, the code shows what the user said
                self.you_said.emit()
                self.sentence.emit(self.sentence_said.capitalize())
                break

            #If there is an error in catching the audio, the code awarns it
            except:
                self.didnt_get.emit()
                time.sleep(2)
                continue

        #It returns the transcription variable for future usage
        return self.sentence_said    

#Setting a class to group the functions responsible for catching the language for the translation
class Language_Translation (QObject):

    #Setting the signals to link this class to the Window one in order to show on the screen
    #the labels set in the later class mentioned
    finished = Signal()
    forth_screen_interface = Signal()
    lang_not_in_dic = Signal()
    lang_in_dic = Signal()
    only_lang = Signal(str)
    show_lang_in_dic = Signal()
    didnt_get = Signal()
    language_trans = Signal()

    #Starts the function to catch the language for the translation
    def translating(self):

        #Setting a list of languages
        self.dic = ('afrikaans', 'af', 'albanian', 'sq', 
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

        #Sets up the user microphone
        mic = sr.Microphone()
        recg = sr.Recognizer()
         
        #The code enters in a while loop until it gets the language
        while True:
            #Using the microphone
            with mic as source:
                #Controling the room noise
                recg.adjust_for_ambient_noise(source)
                #Setting a flag to tell the user to start talking
                self.forth_screen_interface.emit()
                #Storing what was said in the variable "audio"
                audio = recg.listen(source)

        #From this moment, the code will try to interpret the audio

            try:
                #Sending the audio to the algorithm to recognize voice patterns in English
                lang = recg.recognize_google(audio, language='en')
                
                #Then, if the language said doesn't match with any of the options in the dictionary, 
                #the user will know it, and will be asked to say it again.
                if (lang.lower() not in self.dic):
                    self.lang_not_in_dic.emit()
                    time.sleep(3)
                    continue
                #On the other hand, if the language matches with some of the options in the dictionary, 
                #the code breaks the loop and tell the user the language chosen
                elif (lang.lower() in self.dic):
                    (self.lang_in_dic.emit()) + (self.only_lang.emit(lang))
                    self.show_lang_in_dic.emit()
                    break
            #If there is an error in catching the audio, the code awarns it
            except:
                self.didnt_get.emit()
                time.sleep(2)
                continue

        #Storing the language label
        self.lang_translation = self.dic[self.dic.index(lang.lower())+1]

        #Returns the language label
        return self.lang_translation
    
#Setting a class to group the functions responsible for translating the sentence and playing it
class Speaking_Written_Speech(QObject):
    #Setting the signals to link this class to the Window one in order to show on the screen
    #the labels set in the later class mentioned
    finished = Signal()
    header_trans_sentence = Signal()
    trans_sentence = Signal(str)

    #Defining an __init__ function to initialize the object's arguments
    def __init__(self, language, speech):
        super().__init__()

        self.language = language
        self.speech = speech
    #Defining a function to take the user's written speech and play it in the desired language
    def translating_speech(self):
        #Sending the function "Translator()" to the variable "translator"
        translator = Translator()

        # Translating the written speech
        wr_speech = translator.translate(text = self.speech, dest = self.language)
        #Taking only the "text" part (the translated written speech) from the 
        #"translate" function
        wr_speech = wr_speech.text
        
        #Sending the written_speech file to Google Translate
        tts = gTTS(wr_speech,lang=self.language)
        #Saving the audio file
        tts.save('/home/torizon/sentence.mp3')
        #Setting the translated sentence to the signal
        self.trans_sentence.emit(wr_speech.capitalize())
        #Show the header and transcripts the audio
        self.header_trans_sentence.emit()
        #Converting the audio file from .mp3 to .wav
        check_output(["ffmpeg",'-i', '/home/torizon/sentence.mp3', '-acodec', 'pcm_s16le', '-f', 's16le', '-ac', '1', '-ar', '44100', '/home/torizon/sentence.wav'])
        #Playing the audio
        check_output(["aplay", '-Dplughw:1,0', '-f', 'S16_LE', '-r', '44100', '-c', '1', '/home/torizon/sentence.wav'])

    


#Here it is set the main class, which provides the graphical interface
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        #Setting a Widget to support the layout of the screen
        self.base = QWidget()
        #Setting the layout to show the labels and buttons in a vertical order
        self.layout = QVBoxLayout()

        #Setting a font for headers 
        self.font1 = QFont()
        self.font1.setPixelSize(50)

        #Setting a font for general use labels
        self.font2 = QFont()
        self.font2.setPixelSize(25)

        #Sets the header label, its alignment to the center of the screen, and the font
        self.label_voice_trans = QLabel('Voice Translator')
        self.label_voice_trans.setAlignment(Qt.AlignCenter)
        self.label_voice_trans.setFont(self.font1)
        
        #Sets the button to start the translation program
        self.start_btn = QPushButton('Start translating!') 

        #Sets a button to go to the screen in which the code takes what the user says
        self.next_btn = QPushButton('Next')

        #Sets another "Next" button to link to the screen in which the code takes the language for the translation
        self.next_btn_2 = QPushButton('Next')
        
        #Sets another "Next" button to link to the screen in which the code emits what the user said in the desired language
        self.next_btn_3 = QPushButton('Next') 

        #Sets a button to go back to the main screen and start the process again
        self.restart_btn = QPushButton('Restart') 

        #Defining the labels descriptions
        self.label_speak_say = "Say in English the language you want to speak: "
        self.label_speak_tell_language = "The language in which you want to speak is: "
        self.label_speak_language = ""
        self.label_wrong_language = "The language in which you are trying to speak is either not\na language or is currently not available. \n\nPlease, try again."
        self.label_understand = "I didn’t get it. Please, try again."
        self.label_listening_say = "Say something: "
        self.label_listening_you_said = "You said: "
        self.label_listening_sentence = ""
        self.label_trans_say = "Say in English the language you want for the translation: "
        self.label_trans_tell_language = "The language you want for the translation is: "
        self.label_trans_language = ""
        self.label_header_sentence_translated = "Here is the translated sentence:"
        self.label_translated_sentence = ""
        
        #Setting the labels
        self.say_language_speak = QLabel(self.label_speak_say)
        self.say_language_speak.setAlignment(Qt.AlignCenter)
        self.say_language_speak.setFont(self.font2)
        self.language_speak_is = QLabel(self.label_speak_tell_language)
        self.language_speak_is.setAlignment(Qt.AlignCenter)
        self.language_speak_is.setFont(self.font2)
        self.language_for_speech = QLabel(self.label_speak_language)
        self.language_for_speech.setAlignment(Qt.AlignCenter)
        self.language_for_speech.setFont(self.font1)
        self.wrong_language_selected = QLabel(self.label_wrong_language)
        self.wrong_language_selected.setAlignment(Qt.AlignCenter)
        self.wrong_language_selected.setFont(self.font2)
        self.say_something = QLabel(self.label_listening_say)
        self.say_something.setAlignment(Qt.AlignCenter)
        self.say_something.setFont(self.font2)
        self.you_said = QLabel(self.label_listening_you_said)
        self.you_said.setAlignment(Qt.AlignCenter)
        self.you_said.setFont(self.font2)
        self.sentence = QLabel(self.label_listening_sentence)
        self.sentence.setAlignment(Qt.AlignCenter)
        self.sentence.setFont(self.font2)
        self.say_language_trans = QLabel(self.label_trans_say)
        self.say_language_trans.setAlignment(Qt.AlignCenter)
        self.say_language_trans.setFont(self.font2)
        self.language_trans_is = QLabel(self.label_trans_tell_language)
        self.language_trans_is.setAlignment(Qt.AlignCenter)
        self.language_trans_is.setFont(self.font2)
        self.language_for_trans = QLabel(self.label_trans_language)
        self.language_for_trans.setAlignment(Qt.AlignCenter)
        self.language_for_trans.setFont(self.font2)
        self.header_trans_sentence = QLabel(self.label_header_sentence_translated)
        self.header_trans_sentence.setAlignment(Qt.AlignCenter)
        self.header_trans_sentence.setFont(self.font2)
        self.translated_sentence = QLabel(self.label_translated_sentence)
        self.translated_sentence.setAlignment(Qt.AlignCenter)
        self.translated_sentence.setFont(self.font2)
        self.didnt_get_it = QLabel(self.label_understand)
        self.didnt_get_it.setAlignment(Qt.AlignCenter)
        self.didnt_get_it.setFont(self.font2)
        

        #Sets the background color of the language for the speech according to the RGB color wheel 
        self.language_for_speech.setAutoFillBackground(True)
        color  = QColor(248, 131, 121)
        values = "{r}, {g}, {b}".format(r = color.red(),
                                            g = color.green(),
                                            b = color.blue(),
                                            )
        self.language_for_speech.setStyleSheet("QLabel { background-color: rgb("+values+"); }")

        
        #Sets the background color of the sentence said according to the RGB color wheel
        self.sentence.setAutoFillBackground(True) # This is important!!
        color  = QColor(248, 131, 121)
        values = "{r}, {g}, {b}".format(r = color.red(),
                                            g = color.green(),
                                            b = color.blue(),
                                            )
        self.sentence.setStyleSheet("QLabel { background-color: rgb("+values+"); }")

        #Sets the background color of the language for the translation according to the RGB color wheel 
        self.language_for_trans.setAutoFillBackground(True)
        color  = QColor(248, 131, 121)
        values = "{r}, {g}, {b}".format(r = color.red(),
                                            g = color.green(),
                                            b = color.blue(),
                                            )
        self.language_for_trans.setStyleSheet("QLabel { background-color: rgb("+values+"); }")

        #Sets the background color of the translation sentence according to the RGB color wheel 
        self.translated_sentence.setAutoFillBackground(True)
        color  = QColor(248, 131, 121)
        values = "{r}, {g}, {b}".format(r = color.red(),
                                            g = color.green(),
                                            b = color.blue(),
                                            )
        self.translated_sentence.setStyleSheet("QLabel { background-color: rgb("+values+"); }")

        #Adding the labels and buttons to the layout
        self.layout.addWidget(self.label_voice_trans)
        self.layout.addWidget(self.start_btn)
        self.layout.addWidget(self.say_language_speak)
        self.layout.addWidget(self.language_speak_is)
        self.layout.addWidget(self.language_for_speech)
        self.layout.addWidget(self.wrong_language_selected)
        self.layout.addWidget(self.say_language_trans)
        self.layout.addWidget(self.language_trans_is)
        self.layout.addWidget(self.language_for_trans)
        self.layout.addWidget(self.didnt_get_it)
        self.layout.addWidget(self.say_something)
        self.layout.addWidget(self.you_said)
        self.layout.addWidget(self.sentence)
        self.layout.addWidget(self.header_trans_sentence)
        self.layout.addWidget(self.translated_sentence)
        self.layout.addWidget(self.next_btn)
        self.layout.addWidget(self.next_btn_2)
        self.layout.addWidget(self.next_btn_3)
        self.layout.addWidget(self.restart_btn)

        #Hiding the labels and buttons to be shown later
        self.say_language_speak.hide()
        self.language_speak_is.hide()
        self.language_for_speech.hide()
        self.wrong_language_selected.hide()
        self.say_language_trans.hide()
        self.language_trans_is.hide()
        self.language_for_trans.hide()
        self.didnt_get_it.hide()
        self.say_something.hide()
        self.you_said.hide()
        self.sentence.hide()
        self.header_trans_sentence.hide()
        self.translated_sentence.hide()
        self.next_btn.hide()
        self.next_btn_2.hide()
        self.next_btn_3.hide()
        self.restart_btn.hide()

        #Setting the layout to the Widget
        self.base.setLayout(self.layout)
        #Centralizes the screen
        self.setCentralWidget(self.base)
        #Maximizes the screen size
        self.setWindowState(Qt.WindowMaximized)

        #When the "Start translating!" button is clicked, it links to the function "language_speaking"
        #which will start the function "speak" inside the class "Language_Speak", and gets the language for the speech
        self.start_btn.clicked.connect(self.language_speaking)
        #When the "Next" button is clicked, it links to the function "listening_speech" which will start 
        #the function "listen" inside the class "Listening", and gets what the user says
        self.next_btn.clicked.connect(self.listening_speech)
        #When the other "Next" button is clicked, it links to the function "language_trans" which will 
        #start the function "translating" inside the class "Language_Translation", and gets the language for the translation
        self.next_btn_2.clicked.connect(self.language_trans)
        #When the other "Next" button is clicked, it links to the function "translated_speech" which will 
        #start the function "translating_speech_and_speaking" inside the class "Speaking_Written_Speech", and emits the translated sentence
        self.next_btn_3.clicked.connect(self.translated_speech)
        #When the "Restart" button is clicked, it links to the function "backward_first_screen" which will 
        #bring back the main screen to start the process again
        self.restart_btn.clicked.connect(self.backward_first_screen)

    #Function to link to the "Language_Speak" class
    def language_speaking(self):
        #Creating a QThread object
        self.thread_1 = QThread()
        #Creating a worker object
        self.lang_speak = Language_Speak()
        #Moving worker to the thread
        self.lang_speak.moveToThread(self.thread_1)
        #Setting what the signals will trigger on the screen
        self.lang_speak.sec_screen_interface.connect(self.label_voice_trans.hide)
        self.lang_speak.sec_screen_interface.connect(self.start_btn.hide)
        self.lang_speak.sec_screen_interface.connect(self.say_language_speak.show)
        self.lang_speak.sec_screen_interface.connect(self.wrong_language_selected.hide)
        self.lang_speak.sec_screen_interface.connect(self.didnt_get_it.hide)
        self.lang_speak.sec_screen_interface.connect(self.restart_btn.show)
        self.lang_speak.lang_in_dic.connect(self.say_language_speak.hide)
        self.lang_speak.only_lang.connect(self.language_for_speech.setText)
        self.lang_speak.show_lang_in_dic.connect(self.language_speak_is.show)
        self.lang_speak.show_lang_in_dic.connect(self.language_for_speech.show)
        self.lang_speak.show_lang_in_dic.connect(self.next_btn.show)
        self.lang_speak.lang_not_in_dic.connect(self.say_language_speak.hide)
        self.lang_speak.lang_not_in_dic.connect(self.wrong_language_selected.show)
        self.lang_speak.didnt_get.connect(self.say_language_speak.hide)
        self.lang_speak.didnt_get.connect(self.didnt_get_it.show)
        
        #Connecting signals and slots
        self.thread_1.started.connect(self.lang_speak.speak)
        self.lang_speak.finished.connect(self.thread_1.quit)
        self.restart_btn.clicked.connect(self.thread_1.quit)
        self.lang_speak.finished.connect(self.lang_speak.deleteLater)
        self.thread_1.finished.connect(self.thread_1.deleteLater)
        #Starts the thread
        self.thread_1.start()

    #Function to link to the "Listening" class
    def listening_speech(self):
        #Creating a QThread object
        self.thread_2 = QThread()
        #Creating a worker object
        self.listening = Listening()
        #Moving worker to the thread
        self.listening.moveToThread(self.thread_2)
        #Setting what the signals will trigger
        self.lang_speak.language.connect(self.listening.listen)
        self.listening.say_something.connect(self.language_speak_is.hide)
        self.listening.say_something.connect(self.language_for_speech.hide)
        self.listening.say_something.connect(self.next_btn.hide) 
        self.listening.say_something.connect(self.say_something.show)
        self.listening.say_something.connect(self.didnt_get_it.hide)
        self.listening.you_said.connect(self.say_something.hide)
        self.listening.you_said.connect(self.you_said.show)
        self.listening.you_said.connect(self.sentence.show)
        self.listening.sentence.connect(self.sentence.setText)
        self.listening.you_said.connect(self.next_btn_2.show)
        self.listening.didnt_get.connect(self.say_something.hide)
        self.listening.didnt_get.connect(self.didnt_get_it.show)

        #Connecting signals and slots
        self.thread_2.started.connect(self.lang_speak.send_lang_label)
        self.listening.finished.connect(self.thread_2.quit)
        self.restart_btn.clicked.connect(self.thread_2.quit)
        self.listening.finished.connect(self.listening.deleteLater)
        self.thread_2.finished.connect(self.thread_2.deleteLater)
        #Starts the thread
        self.thread_2.start()

    #Function to link to the "Language_Translation" class
    def language_trans(self):
        #Creating a QThread object
        self.thread_3 = QThread()
        #Creating a worker object
        self.lang_trans = Language_Translation()
        #Moving worker to the thread
        self.lang_trans.moveToThread(self.thread_3)
        #Setting what the signals will trigger on the screen
        self.lang_trans.forth_screen_interface.connect(self.you_said.hide)
        self.lang_trans.forth_screen_interface.connect(self.sentence.hide)
        self.lang_trans.forth_screen_interface.connect(self.say_language_trans.show)
        self.lang_trans.forth_screen_interface.connect(self.wrong_language_selected.hide)
        self.lang_trans.forth_screen_interface.connect(self.didnt_get_it.hide)
        self.lang_trans.forth_screen_interface.connect(self.next_btn_2.hide)
        self.lang_trans.lang_in_dic.connect(self.say_language_trans.hide)
        self.lang_trans.only_lang.connect(self.language_for_trans.setText)
        self.lang_trans.show_lang_in_dic.connect(self.language_trans_is.show)
        self.lang_trans.show_lang_in_dic.connect(self.language_for_trans.show)
        self.lang_trans.show_lang_in_dic.connect(self.next_btn_3.show)
        self.lang_trans.lang_not_in_dic.connect(self.say_language_trans.hide)
        self.lang_trans.lang_not_in_dic.connect(self.wrong_language_selected.show)
        self.lang_trans.didnt_get.connect(self.say_language_trans.hide)
        self.lang_trans.didnt_get.connect(self.didnt_get_it.show)
        
        #Connecting signals and slots
        self.thread_3.started.connect(self.lang_trans.translating)
        self.lang_trans.finished.connect(self.thread_3.quit)
        self.restart_btn.clicked.connect(self.thread_3.quit)
        self.lang_trans.finished.connect(self.lang_trans.deleteLater)
        self.thread_3.finished.connect(self.thread_3.deleteLater)
        #Starts the thread
        self.thread_3.start()

    #Function to link to the "Speaking_Written_Speech" class
    def translated_speech(self):
        #Creating a QThread object
        self.thread_4 = QThread()
        #Creating a worker object
        self.speak_wr_speech = Speaking_Written_Speech(language=self.lang_trans.lang_translation,speech=self.listening.sentence_said)
        #Moving worker to the thread
        self.speak_wr_speech.moveToThread(self.thread_4)
        #Setting what the signals will trigger on the screen
        self.speak_wr_speech.header_trans_sentence.connect(self.language_trans_is.hide)
        self.speak_wr_speech.header_trans_sentence.connect(self.language_for_trans.hide)
        self.speak_wr_speech.header_trans_sentence.connect(self.next_btn_3.hide) 
        self.speak_wr_speech.header_trans_sentence.connect(self.header_trans_sentence.show)
        self.speak_wr_speech.trans_sentence.connect(self.translated_sentence.setText)
        self.speak_wr_speech.header_trans_sentence.connect(self.translated_sentence.show)

        #Connecting signals and slots
        self.thread_4.started.connect(self.speak_wr_speech.translating_speech)
        self.speak_wr_speech.finished.connect(self.thread_4.quit)
        self.restart_btn.clicked.connect(self.thread_4.quit)
        self.speak_wr_speech.finished.connect(self.speak_wr_speech.deleteLater)
        self.thread_4.finished.connect(self.thread_4.deleteLater)
        #Starts the thread
        self.thread_4.start()

    #Function to go back to the main screen
    def backward_first_screen(self):
        self.say_language_speak.hide()
        self.language_speak_is.hide()
        self.language_for_speech.hide()
        self.wrong_language_selected.hide()
        self.say_language_trans.hide()
        self.language_trans_is.hide()
        self.language_for_trans.hide()
        self.didnt_get_it.hide()
        self.say_something.hide()
        self.you_said.hide()
        self.sentence.hide()
        self.header_trans_sentence.hide()
        self.translated_sentence.hide()
        self.next_btn.hide()
        self.next_btn_2.hide()
        self.next_btn_3.hide()
        self.restart_btn.hide()
        
        self.label_voice_trans.show()
        self.start_btn.show()

        
#Executing the aplication and the main class
if __name__ == "__main__":

    app = QApplication()

    window = Window()
    window.show()

    app.exec_()