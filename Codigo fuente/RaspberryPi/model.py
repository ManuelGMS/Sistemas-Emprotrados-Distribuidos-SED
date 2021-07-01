import os
import json
from integration import DaoConnection

class Model:
    
    __instance = None

    def __init__(self):
        self.__userConfig = {}

    def getUserConfiguration(self):
        return self.__userConfig

    @staticmethod
    def getInstance():

        if Model.__instance is None:
            Model.__instance = Model()

        return Model.__instance

    def checkIfTempFileExists(self, context):

        context["object"]["exists"] = os.path.isfile('temp.json')

        return context

    def loadUserConfiguration(self):
        
        with open('userConfig.json', 'r') as file: 
            self.__userConfig = json.load(file)
        
    def updateUserConfiguration(self, field, value):
        
        self.__userConfig[field] = value
        
        with open('userConfig.json', 'w') as file:
            json.dump(self.__userConfig, file)
        
    def resetUserConfiguration(self):
        
        data = None
        
        with open('defaultConfig.json', 'r') as file: 
            data = json.load(file)
        
        with open('userConfig.json', 'w') as file: 
            json.dump(data, file)

        self.__userConfig = data
        
    def getMatchConfigurationFromTempFile(self, context):
        
        frame = context["object"]["frame"]
        
        with open('temp.json', 'r') as file: 
            context["object"] = json.load(file)
        
        context["event"] = "SHOW_OLD_MATCH_RESULTS"
        context["object"]["frame"] = frame
        
        return context

    def sendMatchConfiguration(self, context):

        correctConfiguration = False

        if(len(context["object"]["encoder"]) >= 1 and len(context["object"]["encoder"]) <= 16):

            if(len(context["object"]["decoder"]) >= 1 and len(context["object"]["decoder"]) <= 16):

                if(context["object"]["encoder"] != context["object"]["decoder"]):

                    if(context["object"]["code"].isnumeric() and len(context["object"]["code"]) == 4):

                        correctConfiguration = True

                        config = dict()
                        config["code"] = (context["object"]["code"] + "\n").encode('utf-8')
                        config["encoder"] = (context["object"]["encoder"] + "\n").encode('utf-8')
                        config["decoder"] = (context["object"]["decoder"] + "\n").encode('utf-8')
                        
                        if "match" not in context["object"]:

                            config["match"] = { "round" : (str(1) + "\n").encode('utf-8') }
                            config["answer"] = (str(self.__userConfig["answer"]) + "\n").encode('utf-8')
                            config["memory"] = (str(self.__userConfig["memory"]) + "\n").encode('utf-8')
                            config["rounds"] = (str(self.__userConfig["rounds"]) + "\n").encode('utf-8')
                            config["clues"] = (str(int(self.__userConfig["clues"])) + "\n").encode('utf-8')
                            config["sounds"] = (str(int(self.__userConfig["sounds"])) + "\n").encode('utf-8')

                        else:

                            config["answer"] = (str(context["object"]["answer"]) + "\n").encode('utf-8')
                            config["memory"] = (str(context["object"]["memory"]) + "\n").encode('utf-8')
                            config["rounds"] = (str(context["object"]["rounds"]) + "\n").encode('utf-8')
                            config["clues"] = (str(int(context["object"]["clues"])) + "\n").encode('utf-8')
                            config["sounds"] = (str(int(context["object"]["sounds"])) + "\n").encode('utf-8')
                            config["match"] = { "round" : (str(context["object"]["match"]["round"] + 1) + "\n").encode('utf-8') }

                        data = None                    
                        dao = DaoConnection()

                        if dao.writeConfigInSerial(config):

                            data = dao.readDataFromSerial()

                            if data != None:
                                
                                config["match"] = {
                                    "round": data["round"],
                                    "results": (context["object"]["match"]["results"] + data["results"]) if "match" in context["object"] else data["results"],
                                    "selections": (context["object"]["match"]["selections"] + data["selections"]) if "match" in context["object"] else data["selections"]
                                }

                                config["code"] = context["object"]["code"]
                                config["clues"] = self.__userConfig["clues"]
                                config["answer"] = self.__userConfig["answer"]
                                config["memory"] = self.__userConfig["memory"]
                                config["rounds"] = self.__userConfig["rounds"]
                                config["sounds"] = self.__userConfig["sounds"]
                                config["encoder"] = context["object"]["encoder"]
                                config["decoder"] = context["object"]["decoder"]

                                if data["round"] > 0:
                                    
                                    with open('temp.json', 'w') as file: 
                                        json.dump(config, file)

                                context["event"] = "CONNECTION_MISSED"
                    
                            else:

                                if os.path.isfile('temp.json'):

                                    os.remove('temp.json')

                                context["event"] = "GAME_ENDED_CORRECTLY"

                        else:

                            context["event"] = "UNABLE_TO_CONNECT"
                
        if not correctConfiguration:
                    
            context["event"] = "BAD_MATCH_CONFIGURATION"

        return context        
        