#!/usr/bin/env python3
import speech_recognition as sr
from  std_msgs.msg import String 
import rospy
import sys
import time
import signal
from geometry_msgs.msg import Twist
class VoiceControl:
    def __init__(self):     
        self.r = sr.Recognizer()
        self.isAudioAvailable = False
        self.iteration = 0
        self.aliasElapsedTime = 0
        self.alias_time_init = 0
        self.aliasFlag = False       
        signal.signal(signal.SIGINT, self.sigint_handler)

        rospy.init_node('voice_control_node', anonymous=False)
        self.ros_voice_command = rospy.Publisher('voice_recognition/command', String, queue_size=1)

        self.ros_voice_raw = rospy.Publisher('voice_recognition/raw', String, queue_size=1)

        self.get_params()

        self.checkConfig()
 
        rospy.loginfo(self.node_name + " already!")

    def sigint_handler(self, sig, frame):
        print("")

    def get_params(self):

        
        self.node_name = rospy.get_name()
        
        
        param_dict = { self.node_name + "/commands": [''],
                       self.node_name + "/engine": 'sphinx',
                       self.node_name + "/alias": 'robot',
                       self.node_name + "/use_alias": False,
                       self.node_name + "/alias_timeout": 10,
                       self.node_name + "/language": 'en-US'
                      }

        for param in param_dict:

            if rospy.has_param(param):
                param_dict[param] = rospy.get_param(param)
            else:
                rospy.logwarn("Param " + param + " not specified, set to default value: " + str(param_dict.get(param)))

        self.keyword_list = param_dict.get(self.node_name + "/commands")
        self.engine = param_dict.get(self.node_name + "/engine")
        self.alias = param_dict.get(self.node_name + "/alias")
        self.use_alias = param_dict.get(self.node_name + "/use_alias")
        self.aliasTimeout = param_dict.get(self.node_name + "/alias_timeout")
        self.language = param_dict.get(self.node_name + "/language")

    def checkConfig(self):

        engine = "sphinx"
        language = self.language

        if engine == "sphinx":

            if not "en-" in language:
                rospy.logerr("Error: Language " + language + " not supported by Sphinx")
                sys.exit(1)

        else:
                rospy.logerr("Speech recognition engine not found")
                sys.exit(1)

        rospy.loginfo("Working with " + engine + " engine using " + language + " language" )


    def recordAudio(self, source):

        self.isAudioAvailable = False
        audio = 0
        self.iteration+=1
        rospy.loginfo("--------------------------------------")
        rospy.loginfo("Iteration: %s", self.iteration)



        try:
            audio = self.r.listen(source,timeout=5, phrase_time_limit=2)
            self.isAudioAvailable = True
            rospy.loginfo("Audio recording: successful")
        
        except sr.WaitTimeoutError as e:        
            
            rospy.loginfo("Audio recording: timeout; {0}".format(e))

        return audio


    def audioAvailable(self):
        return self.isAudioAvailable


    def findKeyword(self, rawText):

        if self.use_alias:

            if self.alias.lower() in rawText.lower():

                return self.alias

        for keyword in self.keyword_list:


            if keyword.lower() in rawText.lower():


                return keyword
    
        return ''


    def speechRecognition(self, audio):

        rawText = ''
        engine = self.engine 

        if engine == "sphinx":
            rawText = self.getVoiceCommand(audio)

        return rawText

    def getVoiceCommand(self,audio):

        rawText = ''

        
        try:
            rawText = self.r.recognize_sphinx(audio)
            rospy.loginfo("Sphinx thinks you said " + rawText)


        
        except sr.UnknownValueError:
            rospy.loginfo("Sphinx could not understand audio")
        

        return rawText

    def publishRosRaw(self, rawTextDetected):

        self.ros_voice_raw.publish(rawTextDetected)
        rospy.sleep(0.01)

    def publishRos(self, keyword):

        self.ros_voice_command.publish(keyword)
        rospy.sleep(0.01)


    def publishRosAlias(self,keyword):

        if keyword == self.alias:
            
            self.alias_time_init = time.time()
            self.publishRos(self.alias)
            self.aliasFlag = True
            rospy.loginfo("ROS voice command: activated")

        elif self.aliasFlag:

                self.publishRos(keyword)
                self.aliasFlag = False
                rospy.loginfo("ROS voice command: disabled")


    def checkAliasTimeout(self):

        if self.aliasFlag:

            self.aliasElapsedTime = time.time() - self.alias_time_init

            if self.aliasElapsedTime > self.aliasTimeout:

                self.publishRos('')
                self.aliasFlag = False
                rospy.loginfo("ROS voice command: disabled")

    def run(self):

        publisher = rospy.Publisher('/hamer/cmd_vel', Twist, queue_size=1)
        msg = Twist()

        with sr.Microphone(sample_rate=44100) as source:

            self.r.adjust_for_ambient_noise(source) 
            
            while not rospy.is_shutdown():

                audio = self.recordAudio(source)    

                if self.audioAvailable():

                    rawText = self.speechRecognition(audio)
                    self.publishRosRaw(rawText)
                    keyword = self.findKeyword(rawText) 

                    if keyword:
                        rospy.loginfo("Keyword " + keyword + " recognized")
                        if keyword=="go ahead":
                            msg.linear.x=0.4
                            msg.angular.z=0.0
                            publisher.publish(msg)
                        elif keyword=="stop":
                            msg.linear.x=0.0
                            msg.angular.z=0.0
                            publisher.publish(msg)
                        elif keyword=="left":
                            msg.angular.z=0.4
                            msg.linear.x=0.0
                            publisher.publish(msg)
                        elif keyword=="right":
                            msg.angular.z = -0.3
                            msg.linear.x = 0.0
                            publisher.publish(msg)
                        elif keyword=="back":
                            msg.linear.x = -0.3
                            msg.angular.z = 0.0
                            publisher.publish(msg)


                        if(self.use_alias):

                            self.publishRosAlias(keyword)
                        else:

                            self.publishRos(keyword)

                    else:
                        rospy.loginfo("Keyword not recognized")


                self.checkAliasTimeout() 
if __name__ == '__main__':
    voice_control = VoiceControl()
    try:
        voice_control.run()
    except rospy.ROSInterruptException:
        pass
