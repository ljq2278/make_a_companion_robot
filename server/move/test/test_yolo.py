from ultralytics import YOLO
import cv2
# Load the model
model = YOLO('../../../models/yolov8x.pt')  # load a pretrained model

# Perform inference
results = model('../../../aaa.png')

# # Print the results
# results.print()

res_plotted = results[0].plot()
cv2.imshow("result", res_plotted)
tt = 1