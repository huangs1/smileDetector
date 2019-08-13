# Smile Detector

The program's purpose is detect and track smiles through a webcam. The program will launch and start up a window that has an initial video recording that will not be saved anywhere. If there is a smile detected throughout the video, then the program will take a snapshot of that instance and save it to a dropbox folder (that file can be accessed with the link below).

### Instructions to run the program:
- Connect the webcam to your computer if your computer doesn't already have one
- Traverse to the directory with `smileDetector.py`
- Please make sure that you have all the dependencies downloaded
  - python
  - OpenCV (if you are running Ubuntu OS: [use this link](https://www.pyimagesearch.com/2018/05/28/ubuntu-18-04-how-to-install-opencv/) to install OpenCV)
  - imutils
  - dropbox
  - datetime
- Run the following command
```python smileDetector.py --face cascades/haarcascade_frontalface_default.xml --eye cascades/smile.xml --conf conf.json```
- Wait for the program to initialize
- Smile!
- [Click this link to check out your photos in Dropbox](https://www.dropbox.com/sh/l02px37o5v0zxzk/AAAVv9mJrVFRhYuVRmPXCpPYa?dl=0) and previous photos that have been stored from the use of the program. (If you don't want your beautiful smiles to be stored in our database, please email `spencerhuang147@gmail.com` to have your photo removed.)
- Please repeat the last 2 steps to see more of yourself or others
- Just repeat the "Smile!" part if you keep Dropbox open.
- When you are ready to quit, please press q and you will close the window.
