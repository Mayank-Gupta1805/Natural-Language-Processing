from backend.recipe import Recipe
from backend.utils import get_recipes_from_commend
from backend.bot import ask
from backend.constants import RECIPE_COLUMN


class InteractionManager(object):
    def __init__(self, socManager):
        self.socManager = socManager
        self.recipe = None

    def display_single_message(self, message):
        self.socManager.emit_message("voice_command_bot_response", message)

    def display_single_message_user_input(self, message):
        self.socManager.emit_message("voice_command_bot_input", message)

    def display_multiple_messages(self, messages):
        self.socManager.emit_data(
            "voice_command_bot_response_output_multiple", messages)

    def startInteraction(self, command="", returned=False):
        if returned == True:
            while not command:
                question = "What next do you want to do? Else you may exit the conversation."
                self.display_single_message(question)
                command = ask(question)
                if command == 0:
                    return 0
        else:
            if not command:
                question = "What can I do for you?"
                self.display_single_message(question)
                command = ask("What can I do for you?")
            if command == 0:
                self.socManager.emit_message("end_connection", "Goodbye")
                return 0

        self.display_single_message_user_input(command)
        self.recipePrompt(command)

    def recipePrompt(self, command=None):
        while not command:
            command = ask(
                "What are you craving for today? Else say 'Goodbye' to exit.")
            if command == 0:
                self.socManager.emit_message("end_connection", "Goodbye")
                return 0
            self.display_single_message_user_input(command)

        all_recipes, recipe_name = get_recipes_from_commend(command)
        value = 100
        if len(all_recipes) > 1:
            # return json.dumps({"Select": all_recipes})
            message = "Here's what I found, which one do you want to cook? (First/Second/Third...)"
            all_recipe_names = all_recipes[RECIPE_COLUMN].tolist()[:5]
            self.display_multiple_messages(all_recipe_names)
            self.display_single_message(message)

            value = ask(message, all_recipe_names)

            if value == 0:
                self.socManager.emit_message("end_connection", "Goodbye")
                return 0
            if len(set(value.split()).intersection(set(["one", "top", "first", "1", "1st"]))) > 0:
                value = 1
            elif len(set(value.split()).intersection(set(["two", "second", "2nd", "2"]))) > 0:
                value = 2
            elif len(set(value.split()).intersection(set(["three", "third", "3rd", "3"]))) > 0:
                value = 3
            elif len(set(value.split()).intersection(set(["four", "fourth", "4th", "4"]))) > 0:
                value = 4
            elif len(set(value.split()).intersection(set(["five", "fifth", "5th", "5"]))) > 0:
                value = 5
            else:
                value = 1

            self.display_single_message_user_input(value)
            

        recipe = Recipe(self.socManager, all_recipes[all_recipes.index == list(
            all_recipes.index)[value-1]], command, recipe_name)
        self.startInteraction(returned=True)
