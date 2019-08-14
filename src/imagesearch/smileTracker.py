# import the necessary packages
import cv2

class SmileTracker:
	def __init__(self, faceCascadePath, smileCascadePath):
		# load the face and smile detector
		self.faceCascade = cv2.CascadeClassifier(faceCascadePath)
		self.smileCascade = cv2.CascadeClassifier(smileCascadePath)

	def track(self, image):
		# detect faces in the image and initialize the list of
		# rectangles containing the faces and smiles
		faceRects = self.faceCascade.detectMultiScale(image,
			scaleFactor = 1.1, minNeighbors = 10, minSize = (30, 30),
			flags = cv2.CASCADE_SCALE_IMAGE)
		rects = []

		# loop over the face bounding boxes
		for (fX, fY, fW, fH) in faceRects:
			# extract the face ROI and update the list of
			# bounding boxes
			faceROI = image[fY:fY + fH, fX:fX + fW]
			rects.append((fX, fY, fX + fW, fY + fH))

		# return the rectangles representing bounding
		# boxes around the faces
		return rects

	def track2(self, image):
		faceRects = self.faceCascade.detectMultiScale(image,
			scaleFactor = 1.1, minNeighbors = 10, minSize = (30, 30),
			flags = cv2.CASCADE_SCALE_IMAGE)
		rects2 = []
		# loop over the face bounding boxes
		for (fX, fY, fW, fH) in faceRects:
			# extract the face ROI and update the list of
			# bounding boxes
			faceROI = image[fY:fY + fH, fX:fX + fW]

			smileRects = self.smileCascade.detectMultiScale(faceROI,
				scaleFactor = 1.1, minNeighbors = 150, minSize = (40, 40),
				flags = cv2.CASCADE_SCALE_IMAGE)

			# loop over the smile bounding boxes
			for (sX, sY, sW, sH) in smileRects:
				# update the list of boounding boxes
				rects2.append(
					(fX + sX, fY + sY, fX + sX + sW, fY + sY + sH))

		# return the rectangles representing bounding
		# boxes around the smiles
		return rects2
