from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse, HttpRequest, response
import json
import audioToTxt


def index(request):
    if request.method == "POST":
        if not request.POST.get('filename'):
            now = datetime.now()
            date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
            fname = "_video.mp4"
            flname = date_time + fname
            filename = "./video/" + flname
            f = open(filename, 'wb')
            f.write(request.body)
            f.close()
            response = {"data": filename}
            return HttpResponse(json.dumps(response), content_type='application/json')
        if request.POST.get('filename'):
            filepath = request.POST['filename']
            audioToTxt.convertAudio(filepath, 1)
            splitArrayOne = filepath.split('/')
            splitArrayTwo = splitArrayOne[2].split('.')
            txtpath = "./video/txt/" + splitArrayTwo[0] + ".txt"
            f = open(txtpath, 'r')
            file_content = f.read()
            f.close()
            return render(request, 'videoend.html', {
                'texts': file_content,
            })
    if request.method == "GET":
        return render(request, "videoprocc.html")

# Запись видео с помощью OpenCV python
''' 

t_end = tm.time() + 15
fps = 20.0
image_size = (640, 480)
now = datetime.now()
date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
fname = "_vid.avi"
flname = date_time + fname
video_file = "video/" + flname
out = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'XVID'), fps, image_size)


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()
        out.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        out.write(image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


class IPWebCam(object):
    def __init__(self):
        self.url = "http://192.168.1.5:8080/shot.jpg"

    def __del__(self):
        out.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        imgResp = urllib.request.urlopen(self.url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream
        resize = cv2.resize(img, (640, 480), interpolation=cv2.INTER_LINEAR)
        frame_flip = cv2.flip(resize, 1)
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        out.write(frame_flip)
        return jpeg.tobytes()


cam = IPWebCam()


def gen(camera):
    while True:
        frame = cam.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livefe(request):
    try:
        while tm.time() < t_end:
            if tm.time() < t_end:
                return StreamingHttpResponse(gen(IPWebCam()), content_type="multipart/x-mixed-replace;boundary=frame")
            else:
                print("end")
        return render(request, "audioend.html")
    except:  # This is bad! replace it with proper handling
        pass        
'''
