import cv2, time, pandas
from datetime import datetime

### First captured frame
first_frame = None
### Motion status
status_lst = [None, None]
### Stores the times of the change in motion status
times = []
### Creates a DataFrame for the times of motion start and end
df = pandas.DataFrame(columns=["Start", "End"])

### Captures the video
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ### Reads video frame and checks if there is problem
    check, frame = video.read()
    ### Frame amount at the beginning
    status = 0

    ### Turning color frame to a gray scale frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ### Smoothes the frame
    gray = cv2.GaussianBlur(gray, (21,21), 0)

    ### Turning the first_frame to a gray scale frame
    if first_frame is None:
        first_frame = gray
        continue

    ### Delta Frame
    delta_frame = cv2.absdiff(first_frame, gray)
    ### Threshold Frame
    threshold_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    threshold_frame = cv2.dilate(threshold_frame, None, iterations=10)

    ### Finds the contours
    (cnts,_) = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    ### loops through the contours and draws rectangle around the contour that has more contour area than 50000 px
    for contour in cnts:
        if cv2.contourArea(contour) < 40000:
            continue
        status = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)

    ### Appends the times of motion changings to the times array
    status_lst.append(status)

    status_lst = status_lst[-2:]

    if status_lst[-1] == 1 and status_lst[-2] == 0:
        times.append(datetime.now())
    if status_lst[-1] == 0 and status_lst[-2] == 1:
        times.append(datetime.now())

    ### Shows the frames
    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", threshold_frame)
    cv2.imshow("Color Frame", frame)

    ### Delay for frames
    key = cv2.waitKey(1)
    ### If the user presses 'q', the while loop ends and the window gets closed
    if key == ord('q'):
        ### If the motion status becomes active, the time gets added to times array
        if status == 1:
            times.append(datetime.now())
        break

print(status_lst)
print(times)

### loops through the times array and appends the data to the DataFrame
for i in range(0, len(times), 2):
    df = df.append({"Start":times[i], "End":times[i+1]}, ignore_index = True)

### Sends the data in 'df' DataFrame to the times.csv file
df.to_csv("times.csv")

### Closes the video
video.release()
### Closes the open windows
cv2.destroyAllWindows()