from itertools import count
from threading import Thread, Semaphore
import numpy as np
import cv2 as cv
import time 
import random
from datetime import datetime
import os

class Camera(Thread):

    def __init__(self, camId:int, frameWidth:int, frameHeight:int,visualize:bool = False, video_output:bool = False, time_stamped_output:bool = False, root_path:str="",fileName:str="",fileName_postfix:str="", autofocus:bool=False):
        Thread.__init__(self)
        self.camId = camId
        self.width = frameWidth
        self.height = frameHeight
        self.outputfile = fileName
        self.fileName_postfix = fileName_postfix
        self.done = False
        self.image_format = '.jpeg'
        self.autofocus = autofocus
        self.fourcc =  cv.VideoWriter.fourcc('M','J','P','G')
        self.calibration_frames_number = 200
        self.time_stamped_output = time_stamped_output
        self.video_output = video_output
        self.root_path = root_path
        
        if not self.outputfile:
            self.outputfile = self.get_time_stamp()+"_cam"+str(self.camId)+self.fileName_postfix+".mp4"

        self.visualize = visualize

    def connect(self):
        # make sure build and install opencv from source to work with DirectShow on windows
        self.videostreamcapture = cv.VideoCapture(self.camId, cv.CAP_DSHOW)
        self.input_fps  = self.videostreamcapture.get(cv.CAP_PROP_FPS)
        self.recording_fps = self.input_fps
        
        #self.videostreamcapture.set(cv.CAP_PROP_SETTINGS, 1)
        #self.videostreamcapture.set(cv.CAP_PROP_FPS, 30)
        self.videostreamcapture.set(cv.CAP_PROP_FRAME_WIDTH, self.width)
        self.videostreamcapture.set(cv.CAP_PROP_FRAME_HEIGHT, self.height)
        #Todo: seperate recording fps from input fps in future versions

        if not self.autofocus:
            self.videostreamcapture.set(cv.CAP_PROP_AUTOFOCUS, 0) # turn the autofocus off
        else:
            self.videostreamcapture.set(cv.CAP_PROP_AUTOFOCUS, 1) # turn the autofocus on


    def calculate_camera_fps(self)->int:
          
        start_tick = cv.getTickCount()
        for i in range(0, self.calibration_frames_number) :
            ret, frame = self.videostreamcapture.read()
        end_tick = cv.getTickCount()
        time_taken = (end_tick - start_tick) / cv.getTickFrequency() 
        fps  = self.calibration_frames_number / time_taken
        return fps
    
    def calculate_recording_fps(self)->int:
         
        outputstreamwriter = cv.VideoWriter(self.root_path+self.get_time_stamp()+"_calibration_"+str(self.camId)+self.fileName_postfix+".mp4",  self.fourcc, 30, (self.width, self.height), isColor=True)
        #ends= cv.videoio_registry.getBackends()
        print("backends:"+outputstreamwriter.getBackendName())
        start_tick = cv.getTickCount()
        for i in range(0, self.calibration_frames_number) :
            ret, frame = self.videostreamcapture.read()
            outputstreamwriter.write(frame)
            #cv.imwrite(str(random.random())+'.png', frame)
            #cv.imshow('Camera Index:'+ str(self.camId), frame)
            cv.waitKey(1)
        end_tick = cv.getTickCount()
        time_taken = (end_tick - start_tick) / cv.getTickFrequency() 
        fps  = self.calibration_frames_number / time_taken
        outputstreamwriter.release()
        return fps
    def get_time_stamp(self):
        timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S.%f')[:-3]
        return timestamp

    def run(self):

        camera_fps = self.calculate_camera_fps()
        print("camera fps: " + str(camera_fps))

        if self.time_stamped_output:
            date_path=self.root_path + datetime.now().strftime('%Y-%m-%d')
            if not os.path.exists(date_path):
                os.mkdir(date_path) 

        if self.video_output:
            recording_fps = self.calculate_recording_fps()           
            print("recording fps: " + str(recording_fps))
            self.outputstreamwriter = cv.VideoWriter(self.root_path + self.outputfile, self.fourcc, recording_fps, (self.width, self.height), isColor=True)

        while not self.done:
            ret, frame = self.videostreamcapture.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break  
            
            if self.time_stamped_output:
                timestamp = self.get_time_stamp()
                cv.imwrite(date_path + "/" + timestamp +"_"+str(cv.getTickCount())+"_"+ "cam" +str(self.camId)+self.fileName_postfix+ self.image_format, frame)
                
                # FFMPEG-> slow recording        -> .\ffmpeg.exe -y -f vfwcap -r 30 -i 0 out.mp4
                # FFMPEG-> list of devices       -> .\ffmpeg.exe -list_devices true -f dshow -i dummy
                # FFMPEG-> fast recording camera -> .\ffmpeg.exe -f dshow -video_size 1280x720 -t 00:00:30 -i video="Logitech StreamCam" out.mp4
            
            if self.video_output:
                self.outputstreamwriter.write(frame)

            if self.visualize:  
                cv.imshow('Camera Index:'+ str(self.camId), frame)
            
            cv.waitKey(1)

        self.videostreamcapture.release()
        if self.video_output:
            self.outputstreamwriter.release()
        cv.destroyAllWindows()

    def stopit(self):
        self.done = True