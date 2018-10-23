import threading
from random import random
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import imutils
import time
import dlib
import cv2
import datetime
from Evento import Evento

class visualRecognition(threading.Thread):
    # aca va todo el codigo de visual recognition

	def __init__(self, events, lock, args):
		threading.Thread.__init__(self)
		self.events = events
		self.lock = lock
		self.args = args

		 
		# define two constants, one for the eye aspect ratio to indicate
		# blink and then a second constant for the number of consecutive
		# frames the eye must be below the threshold for to set off the
		# alarm
		self.EYE_AR_THRESH = 0.3
		self.EYE_AR_CONSEC_FRAMES_SLEEP = 16
		self.EYE_AR_CONSEC_FRAMES_BLINK = 3

		# initialize the frame counter as well as a boolean used to
		# indicate if the alarm is going off
		self.COUNTER = 0
		self.TOTAL = 0
		self.ALARM_ON = False

		# load OpenCV's Haar cascade for face detection (which is faster than
		# dlib's built-in HOG detector, but less accurate), then create the
		# facial landmark predictor
		print("[INFO] loading facial landmark predictor...")
		self.detector = cv2.CascadeClassifier(args["cascade"])
		self.predictor = dlib.shape_predictor(args["shape_predictor"])

		# grab the indexes of the facial landmarks for the left and
		# right eye, respectively
		(self.lStart, self.lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
		(self.rStart, self.rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

		# start the video stream thread
		print("[INFO] starting video stream thread...")
		#self.vs = VideoStream(src=0).start()
		self.vs = VideoStream(usePiCamera=True).start()
		time.sleep(1.0)

	def run(self):
		time = datetime.datetime.now()
		while True:
			# grab the frame from the threaded video file stream, resize
			# it, and convert it to grayscale
			# channels)
			frame = self.vs.read()
			frame = imutils.resize(frame, width=450)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			# detect faces in the grayscale frame
			rects = self.detector.detectMultiScale(gray, scaleFactor=1.1, 
			minNeighbors=5, minSize=(30, 30),
			flags=cv2.CASCADE_SCALE_IMAGE)

			# loop over the face detections
			for (x, y, w, h) in rects:
				# construct a dlib rectangle object from the Haar cascade
				# bounding box
				rect = dlib.rectangle(int(x), int(y), int(x + w),
				int(y + h))

				# determine the facial landmarks for the face region, then
				# convert the facial landmark (x, y)-coordinates to a NumPy
				# array
				shape = self.predictor(gray, rect)
				shape = face_utils.shape_to_np(shape)
				# extract the left and right eye coordinates, then use the
				# coordinates to compute the eye aspect ratio for both eyes
				leftEye = shape[self.lStart:self.lEnd]
				rightEye = shape[self.rStart:self.rEnd]
				leftEAR = self.eye_aspect_ratio(leftEye)
				rightEAR = self.eye_aspect_ratio(rightEye)

				# average the eye aspect ratio together for both eyes
				ear = (leftEAR + rightEAR) / 2.0

				# compute the convex hull for the left and right eye, then
				# visualize each of the eyes
				leftEyeHull = cv2.convexHull(leftEye)
				rightEyeHull = cv2.convexHull(rightEye)
				cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
				cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

				# check to see if the eye aspect ratio is below the blink
				# threshold, and if so, increment the blink frame counter
				if ear < self.EYE_AR_THRESH:
					self.COUNTER += 1
					# if the eyes were closed for a sufficient number of
					# frames, then sound the alarm
					if self.COUNTER >= self.EYE_AR_CONSEC_FRAMES_BLINK:

						self.TOTAL += 1
						now = datetime.datetime.now()
						if now.minute == time.minute:
							if (now.second - time.second) > 10:
								self.TOTAL = 0
								time = now
						else: 
							dif = 60 + (now.second - time.second)
							if dif > 10:
								self.TOTAL = 0 
								time = now
						print("Blinks: ", self.TOTAL)

					if self.COUNTER >= self.EYE_AR_CONSEC_FRAMES_SLEEP:
						self.events.put(Evento("ALERT", "Dormido", "Conductor"))
						if not self.ALARM_ON:
							self.ALARM_ON = True

							# check to see if the TrafficHat buzzer should
							# be sounded
							if self.args["alarm"] > 0:
								th.buzzer.blink(0.1, 0.1, 10, background=True)

							# draw an alarm on the frame
							cv2.putText(frame, "DROWSINESS ALERT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				# reset the eye frame counter
				# otherwise, the eye aspect ratio is not below the blink
				# threshold, so reset the counter and alarm
				else:
					self.COUNTER = 0
					self.ALARM_ON = False

				# draw the computed eye aspect ratio on the frame to help
				# with debugging and setting the correct eye aspect ratio
				# thresholds and frame counters
				cv2.putText(frame, "EAR: {:.3f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

			# show the frame
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF

			# if the `q` key was pressed, break from the loop
			if key == ord("q"):
				break

		# do a bit of cleanup
		cv2.destroyAllWindows()
		vs.stop()

	def euclidean_dist(self, ptA, ptB):
		# compute and return the euclidean distance between the two
		# points
		return np.linalg.norm(ptA - ptB)

	def eye_aspect_ratio(self, eye):
		# compute the euclidean distances between the two sets of
		# vertical eye landmarks (x, y)-coordinates
		A = self.euclidean_dist(eye[1], eye[5])
		B = self.euclidean_dist(eye[2], eye[4])

		# compute the euclidean distance between the horizontal
		# eye landmark (x, y)-coordinates
		C = self.euclidean_dist(eye[0], eye[3])

		# compute the eye aspect ratio
		ear = (A + B) / (2.0 * C)

		# return the eye aspect ratio
		return ear