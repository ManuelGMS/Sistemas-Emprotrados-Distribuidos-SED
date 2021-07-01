from model import Model

class Controller:

    __instance = None

    @staticmethod
    def getInstance():

        if Controller.__instance is None:
            Controller.__instance = Controller()

        return Controller.__instance

    def action(self, context):

        if context["event"] == "INITALIZE":

            model = Model.getInstance()

            model.loadUserConfiguration()

        elif context["event"] == "LOAD_USER_CONFIGURATION":

            context["object"]["config"] = Model.getInstance().getUserConfiguration() 

            context["object"]["frame"].updateFrame(context)

        elif context["event"] == "UPDATE_USER_CONFIGURATION":

            Model.getInstance().updateUserConfiguration(context["object"]["field"],context["object"]["value"])

            context["object"]["config"] = Model.getInstance().getUserConfiguration() 

            context["object"]["frame"].updateFrame(context)

        elif context["event"] == "RESET_USER_CONFIGURATION":

            Model.getInstance().resetUserConfiguration()

            context["object"]["config"] = Model.getInstance().getUserConfiguration() 

            context["object"]["frame"].updateFrame(context)

        elif context["event"] == "PLAY_GAME":

            context = Model.getInstance().sendMatchConfiguration(context)

            context["object"]["frame"].updateFrame(context)
            
        elif context["event"] == "ACTIVATE_DEACTIVATE_RESTABLISH_MATCH_BUTTON":

            context = Model.getInstance().checkIfTempFileExists(context)

            context["object"]["frame"].updateFrame(context)

        elif context["event"] == "RESTABLISH_MATCH":

            context = Model.getInstance().getMatchConfigurationFromTempFile(context)

            context["object"]["frame"].updateFrame(context)

            context = Model.getInstance().sendMatchConfiguration(context)

            context["object"]["frame"].updateFrame(context)

        elif context["event"] == "CLEAN_FRAME_ENTRIES":

            context["object"]["frame"].updateFrame(context)