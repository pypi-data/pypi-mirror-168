import time
import os
from pkg_resources import resource_filename
import cv2
import numpy as np
import pytesseract
from imutils.object_detection import non_max_suppression
import urllib
from DocTest.utils.east import decode

class PyTextractor:
    layer_names = ('feature_fusion/Conv_7/Sigmoid', 'feature_fusion/concat_3',)

    def __init__(self, east=None):
        pkg_east_model = resource_filename(__name__, 'data/frozen_east_text_detection.pb')
        self.east = east or pkg_east_model
        self._load_assets()

    def get_image_text(self,
                       image,
                       width=320,
                       height=320,
                       numbers=True,
                       confThreshold=0.5,
                       nmsThreshold=0.4,
                       percentage=2.0,
                       min_boxes=1,
                       max_iterations=20,
                       **kwargs):
        loaded_image = image
        (origH, origW) = loaded_image.shape[:2]

        image, width, height, ratio_width, ratio_height = self._resize_image(
            loaded_image, width, height
        )
        scores, geometry = self._compute_scores_geometry(image, width, height)
        [boxes, confidences] = decode(scores, geometry, confThreshold)

        # Apply NMS
        indices = cv2.dnn.NMSBoxesRotated(
            boxes, confidences, confThreshold, nmsThreshold
        )
        


        # results is dictionary with keys: left, top, width, height, text
        results = {}
        results['text'] = []
        results['left'] = []
        results['top'] = []
        results['width'] = []
        results['height'] = []
        rotated_boxes = []
        for i in indices:
            # get 4 corners of the rotated rect
            vertices = cv2.boxPoints(boxes[i])
            # scale the bounding box coordinates based on the respective ratios
            for j in range(4):
                vertices[j][0] *= ratio_width
                vertices[j][1] *= ratio_height

            rect = cv2.boundingRect(vertices)
            startX = max(0, rect[0])
            startY = max(0, rect[1])
            endX = min(origW, rect[0] + rect[2])
            endY = min(origH, rect[1] + rect[3])
            rotated_boxes.append((startX, startY, endX, endY))
        # # Use non_max_suppression to get rid of overlapping boxes
        # boxes = non_max_suppression(np.array(rotated_boxes), probs=None, overlapThresh=0.5)
        # merge overlapping boxes
        boxes = self._merge_close_boxes(rotated_boxes, percentage)

        for (startX, startY, endX, endY) in boxes:
            # extract the actual padded ROI
            roi = loaded_image[startY:endY, startX:endX]
            config = ("-l eng --oem 1 --psm 7")
            text = pytesseract.image_to_string(roi, config=config)
            # add the bounding box coordinates and OCR'd text to the list
            # of results
            results['text'].append(text)
            results['left'].append(startX)
            results['top'].append(startY)
            results['width'].append(endX - startX)
            results['height'].append(endY - startY)
        return results

    def _merge_close_boxes(self, boxes, percentage=2.0):
        # merge overlapping boxes
        merged_boxes = []
        for box in boxes:
            if not merged_boxes:
                merged_boxes.append(box)
            else:
                for merged_box in merged_boxes:
                    if self._is_close(box, merged_box, percentage):
                        merged_box = self._merge_boxes(box, merged_box)
                        break
                else:
                    merged_boxes.append(box)
        return merged_boxes

    def _merge_boxes(self, box1, box2):
        """
        returns merged box
        """
        (x1, y1, w1, h1) = box1
        (x2, y2, w2, h2) = box2
        x = min(x1, x2)
        y = min(y1, y2)
        w = max(x1 + w1, x2 + w2) - x
        h = max(y1 + h1, y2 + h2) - y
        return (x, y, w, h)

    def _is_close(self, box1, box2, percentage=2.0):
        """
        returns True if boxes are overlapping or if boxes are close to each other (lesser than percentage of width or height)
        """
        (x1, y1, w1, h1) = box1
        (x2, y2, w2, h2) = box2
        # check if boxes are overlapping
        if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
            return True
        # check if boxes are close to each other
        if abs(x1 - x2) < w1 * percentage / 100 or abs(y1 - y2) < h1 * percentage / 100:
            return True
        return False


    def _load_image(self, image):
        return cv2.imread(image)

    def _resize_image(self, image, width, height):
        (H, W) = image.shape[:2]

        (newW, newH) = (width, height)
        ratio_width = W / float(newW)
        ratio_height = H / float(newH)


        # resize the image and grab the new image dimensions
        resized_image = cv2.resize(image, (newW, newH))
        (H, W) = resized_image.shape[:2]
        return (resized_image, height, width, ratio_width, ratio_height)

    def _compute_scores_geometry(self, image, width, height):
        # construct a blob from the image and then perform a forward pass of
        # the model to obtain the two output layer sets
        blob = cv2.dnn.blobFromImage(
            image, 1.0, (width, height), (123.68, 116.78, 103.94), swapRB=True, crop=False
        )
        start = time.time()
        self.east_net.setInput(blob)
        (scores, geometry) = self.east_net.forward(self.layer_names)
        end = time.time()

        # show timing information on text prediction
        print('[INFO] text detection took {:.6f} seconds'.format(end - start))
        return (scores, geometry)

    def _load_assets(self):
        self._get_east()
        start = time.time()
        self.east_net = cv2.dnn.readNet(self.east)
        end = time.time()
        print('[INFO] Loaded EAST text detector {:.6f} seconds ...'.format(end - start))

    def _get_east(self):
        if os.path.exists(self.east):
            return

            # load the pre-trained EAST model for text detection
        pkg_path = os.path.dirname(__file__)
        data_file = os.path.join(pkg_path, self.east)
        os.makedirs(os.path.dirname(data_file), exist_ok=True)

        # check if file abs_east_model_path exists
        if os.path.isfile(data_file) is False:
            # Download from url https://raw.githubusercontent.com/oyyd/frozen_east_text_detection.pb/master/frozen_east_text_detection.pb
            print("Downloading frozen_east_text_detection.pb from url")
            url = "https://raw.githubusercontent.com/oyyd/frozen_east_text_detection.pb/master/frozen_east_text_detection.pb"
            urllib.request.urlretrieve(url, data_file)


    def _get_boxes(self, num_rows, num_cols, confidence, geometry, scores, min_boxes, max_iterations):
        iterations = 0
        boxes = []
        rects = []
        confidences = []
        while(iterations < max_iterations):
            for y in range(0, num_rows):
                # extract the scores (probabilities), followed by the geometrical
                # data used to derive potential bounding box coordinates that
                # surround text
                scores_data = scores[0, 0, y]
                x_data_0 = geometry[0, 0, y]
                x_data_1 = geometry[0, 1, y]
                x_data_2 = geometry[0, 2, y]
                x_data_3 = geometry[0, 3, y]
                angles_data = geometry[0, 4, y]

                # loop over the number of columns
                for x in range(0, num_cols):
                    # if our score does not have sufficient probability, ignore it
                    if scores_data[x] < confidence:
                        continue

                    # compute the offset_ factor as our resulting feature maps will
                    # be 4x smaller than the input image
                    (offset_X, offset_Y) = (x * 4.0, y * 4.0)

                    # extract the rotation angle for the prediction and then
                    # compute the sin and cosine
                    angle = angles_data[x]
                    cos = np.cos(angle)
                    sin = np.sin(angle)

                    # use the geometry volume to derive the width and height of
                    # the bounding box
                    h = x_data_0[x] + x_data_2[x]
                    w = x_data_1[x] + x_data_3[x]

                    # compute both the start_ing and end_ing (x, y)-coordinates for
                    # the text prediction bounding box
                    end_X = int(offset_X + (cos * x_data_1[x]) + (sin * x_data_2[x]))
                    end_Y = int(offset_Y - (sin * x_data_1[x]) + (cos * x_data_2[x]))
                    start_X = int(end_X - w)
                    start_Y = int(end_Y - h)

                    # add the bounding box coordinates and probability score to
                    # our respective lists
                    rects.append((start_X, start_Y, end_X, end_Y))
                    confidences.append(scores_data[x])

            # apply non-maxima suppression to suppress weak, overlapping bounding
            # boxes
            boxes = non_max_suppression(np.array(rects), probs=confidences)
            if len(boxes) >= min_boxes:
                return boxes
            else:
                confidence /= 2
                print('Couldn\'t find at least {min_boxes} boxe(s), halving confidence to {confidence}'.
                      format(min_boxes=min_boxes, confidence=confidence))

    def _extract_text(self, image, boxes, percent, numbers, ratio_width, ratio_height):
        extracted_text = []
        for (start_X, start_Y, end_X, end_Y) in boxes:
            # scale the bounding box coordinates based on the respective
            # ratios
            percent = (percent / 100 + 1) if percent >= 0 else ((100 - percent) / 100)
            start_X = int(start_X * ratio_width * percent)
            start_Y = int(start_Y * ratio_height * percent)
            end_X = int(end_X * ratio_width * percent)
            end_Y = int(end_Y * ratio_height * percent)

            ROIImage = image.copy()[start_Y:end_Y, start_X:end_X]
            import uuid
            cv2.imwrite(str(uuid.uuid4())+".png", ROIImage)
            config = '--psm 6' if numbers else ''
            extracted_text.append(pytesseract.image_to_string(
                ROIImage, config=config)
            )

        return extracted_text