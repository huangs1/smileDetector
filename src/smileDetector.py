# USAGE
# python smileDetector.py --face cascades/haarcascade_frontalface_default.xml --eye cascades/smile.xml --conf conf.json

# import the necessary packages
from imagesearch.eyetracker import EyeTracker
from imagesearch import imutils
from imagesearch.tempimage import tempimage
import argparse
import warnings
import datetime
import dropbox
import imutils
import json
import time
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", required = True,
	help = "path to where the face cascade resides")
ap.add_argument("-e", "--eye", required = True,
	help = "path to where the eye cascade resides")
ap.add_argument("-v", "--video",
	help = "path to the (optional) video file")
ap.add_argument("-c", "--conf", required=True,
	help="path to the JSON configuration file")
args = vars(ap.parse_args())

# filter warnings, load the configuration and initialize the Dropbox
# client
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))
client = None

# check to see if the Dropbox should be used
if conf["use_dropbox"]:
	# connect to dropbox and start the session authorization process
	client = dropbox.Dropbox(conf["dropbox_access_token"])
	print("[SUCCESS] dropbox account linked")

# allow the camera to warmup, then initialize the average frame, last
# uploaded timestamp, and frame motion counter
print("[INFO] warming up...")
time.sleep(conf["camera_warmup_time"])
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0

# construct the eye tracker
et = EyeTracker(args["face"], args["eye"])

# if a video path was not supplied, grab the reference
# to the gray
if not args.get("video", False):
	camera = cv2.VideoCapture(0)

# otherwise, load the video
else:
	camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
	timestamp = datetime.datetime.now()

	# if we are viewing a video and we did not grab a
	# frame, then we have reached the end of the video
	if args.get("video") and not grabbed:
		break

	# draw the text and timestamp on the frame
	ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
	cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)

	# resize the frame and convert it to grayscale
	frame = imutils.resize(frame, width = 1200)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detect faces and eyes in the image
	rects = et.track(gray)
	text = "No Smiles anywhere"
	# loop over the face bounding boxes and draw them
	for rect in rects:
		cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (0, 255, 0), 2)
		text = "Smile Detected"
		cv2.putText(frame, "Emotion: {}".format(text), (10, 35),
			cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)

	# show the tracked eyes and face
	cv2.imshow("Tracking", frame)

	# check to see if the room is occupied
	if text == "Smile Detected":
		# check to see if enough time has passed between uploads
		if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
			# increment the motion counter
			motionCounter += 1

			# check to see if the number of frames with consistent motion is
			# high enough
			if motionCounter >= conf["min_motion_frames"]:
				# check to see if dropbox sohuld be used
				if conf["use_dropbox"]:
					# write the image to temporary file
					t = tempimage()
					cv2.imwrite(t.path, frame)

					# upload the image to Dropbox and cleanup the tempory image
					print("[UPLOAD] {}".format(ts))
					path = "/{base_path}/{timestamp}.jpg".format(
					    base_path=conf["dropbox_base_path"], timestamp=ts)
					client.files_upload(open(t.path, "rb").read(), path)
					t.cleanup()

				# update the last uploaded timestamp and reset the motion
				# counter
				lastUploaded = timestamp
				motionCounter = 0

	# otherwise, the room is not occupied
	else:
		motionCounter = 0

	# if the 'q' key is pressed, stop the loop
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break

# cleanup the camera and close any open windows
rawCapture.truncate(0)
camera.release()
cv2.destroyAllWindows()
