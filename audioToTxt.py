import speech_recognition as sr
import wave
import librosa
import soundfile as sf


def convertAudio(filepath, type):
    x, _ = librosa.load(filepath, sr=16000)
    if type == 0:
        sf.write('./audio/tmp.wav', x, 16000)
        wave.open('./audio/tmp.wav', 'r')
        filename = "./audio/tmp.wav"
    if type == 1:
        sf.write('./video/tmp.wav', x, 16000)
        wave.open('./video/tmp.wav', 'r')
        filename = "./video/tmp.wav"
    splitArrayOne = filepath.split('/')
    splitArrayTwo = splitArrayOne[2].split('.')
    # initialize the recognizer
    r = sr.Recognizer()

    # open the file
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        print(text)
        if type == 0:
            txtpath = "./audio/txt/" + splitArrayTwo[0] + ".txt"
        if type == 1:
            txtpath = "./video/txt/" + splitArrayTwo[0] + ".txt"
        f = open(txtpath, 'w')
        f.write(text)


