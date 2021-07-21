import json
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, response
from django.shortcuts import get_object_or_404, render
import pyaudio
import wave
from datetime import datetime, date, time
import audioToTxt


def index(request):
    if request.method == "POST":
        if not request.POST.get('filename'):
            now = datetime.now()
            date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
            fname = "_audio.amr"
            flname = date_time + fname
            filename = "./audio/" + flname
            f = open(filename, 'wb')
            f.write(request.body)
            f.close()
            response = {"data": filename}
            return HttpResponse(json.dumps(response), content_type='application/json')
        if request.POST.get('filename'):
            filepath = request.POST['filename']
            audioToTxt.convertAudio(filepath, 0)
            splitArrayOne = filepath.split('/')
            splitArrayTwo = splitArrayOne[2].split('.')
            txtpath = "./audio/txt/" + splitArrayTwo[0] + ".txt"
            f = open(txtpath, 'r')
            file_content = f.read()
            f.close()
            return render(request, 'audioend.html', {
                'texts': file_content,
            })
    if request.method == "GET":
        return render(request, "audioprocc.html")


# Запись аудио с помощью python
'''
def func():
    p = pyaudio.PyAudio()
    chunk = 1024  # Запись кусками по 1024 сэмпла
    sample_format = pyaudio.paInt16  # 16 бит на выборку
    channels = 2
    rate = 44100  # Запись со скоростью 44100 выборок(samples) в секунду
    seconds = 10
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
    fname = "_audio.wav"
    flname = date_time + fname
    filename = "audio/" + flname
    p = pyaudio.PyAudio()  # Создать интерфейс для PortAudio

    print('Recording...')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=rate,
                    frames_per_buffer=chunk,
                    input_device_index=1,  # индекс устройства с которого будет идти запись звука
                    input=True)

    frames = []  # Инициализировать массив для хранения кадров

    # Хранить данные в блоках в течение 10 секунд
    for i in range(0, int(rate / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Остановить и закрыть поток
    stream.stop_stream()
    stream.close()
    # Завершить интерфейс PortAudio
    p.terminate()

    print('Finished recording!')

    # Сохранить записанные данные в виде файла WAV
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
'''
