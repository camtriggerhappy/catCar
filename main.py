from pupil_apriltags import Detector
import cv2
import serial

camera = cv2.VideoCapture(0)

arduino = serial.Serial(baudrate=9600, timeout=1)

at_detector = Detector(
    families="tag36h11",
    nthreads=1,
    quad_decimate=1.0,
    quad_sigma=0.0,
    refine_edges=1,
    decode_sharpening=0.25,
    debug=0
)


def turnRight():
    print("Turning right")
    arduino.write(bytes("right", 'utf-8'))


while True:
    img = camera.read()[1]
    if img is None:
      continue
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    at_detector.detect(gray)
    results = at_detector.detect(gray)
    print("[INFO] {} total AprilTags detected".format(len(results)))

    for r in results:
        # extract the bounding box (x, y)-coordinates for the AprilTag
        # and convert each of the (x, y)-coordinate pairs to integers
        (ptA, ptB, ptC, ptD) = r.corners
        ptB = (int(ptB[0]), int(ptB[1]))
        ptC = (int(ptC[0]), int(ptC[1]))
        ptD = (int(ptD[0]), int(ptD[1]))
        ptA = (int(ptA[0]), int(ptA[1]))
        # draw the bounding box of the AprilTag detection

        # draw the center (x, y)-coordinates of the AprilTag
        center = [(ptA[0] + ptB[0] + ptC[0] + ptD[0]) / 4, (ptA[1] + ptB[1] + ptC[1] + ptD[1]) / 4]

        print(center)
        if (center[0] > img.shape[1] / 2):
            turnRight()
