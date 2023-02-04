from backend.bot import ask, engine_talk
from backend.database import get_information_from_df
from backend.text_preprocessor import sentence_extraction
from backend.utils import get_command_context
from backend.constants import INGREDIENTS_COLUMN, PREPTIME_COLUMN, COOKTIME_COLUMN, SERVING_COLUMN, INSTRUCTIONS_COLUMN, TOTALTIME_COLUMN


class recipeSteps:
    def __init__(self, step, instruction):
        self.step = step
        self.instruction = instruction

    def __str__(self):
        return self.step + " " + self.instruction


class Recipe:
    def __init__(self, socManager, recipe, command, recipe_name):
        self.socManager = socManager
        self.recipe = recipe_name
        self.ingredients = ""
        self._initialise_instructions(recipe)
        self.context_instruction = 0
        self.context_ingredient = 0
        self.command = command
        self._handle_command(recipe, command) 

    def _handle_command(self, recipe, command):

        self.question_context = get_command_context(command)
        self.answer = get_information_from_df(recipe, self.question_context)
        self._handle_ingredients_column()
        self._handle_preptime_column()
        self._handle_cooktime_column()
        self._handle_totaltime_column()
        self._handle_servings_column()
        self._handle_instructions_column()

    def _handle_instructions_column(self):
        if self.question_context != INSTRUCTIONS_COLUMN:
            return
        self.answer = self.instructions
        self.read_instructions_stepwise()

    def _handle_servings_column(self):
        if self.question_context != SERVING_COLUMN:
            return
        response = "The total servings for " + \
            str(self.answer[0][SERVING_COLUMN]) + " people"
        self.socManager.emit_message(
            "voice_command_bot_response", response)
        engine_talk(response)

    def _handle_totaltime_column(self):
        if self.question_context != TOTALTIME_COLUMN:
            return
        response = "The total time is " + \
            str(self.answer[0][TOTALTIME_COLUMN]) + " minutes"
        self.socManager.emit_message(
            "voice_command_bot_response", response)
        engine_talk(response)

    def _handle_cooktime_column(self):
        if self.question_context != COOKTIME_COLUMN:
            return
        response = "The cooking time is " + \
            str(self.answer[0][COOKTIME_COLUMN]) + " minutes"
        self.socManager.emit_message(
            "voice_command_bot_response", response)
        engine_talk(response)

    def _handle_preptime_column(self):
        if self.question_context != PREPTIME_COLUMN:
            return
        response = "The preparation time is " + \
            str(self.answer[0][PREPTIME_COLUMN]) + " minutes"
        self.socManager.emit_message(
            "voice_command_bot_response", response)
        engine_talk(response)

    def _handle_ingredients_column(self):
        if self.question_context != INGREDIENTS_COLUMN:
            return
        self.ingredients = self.answer[0][INGREDIENTS_COLUMN]
        self.ingredients = self.ingredients.split(",")
        self.ingredients = [x.strip() for x in self.ingredients]
        self.ingredients = [x for x in self.ingredients if x]
        self.answer = self.ingredients
        self.read_ingredients_stepwise() # type: ignore

    def _initialise_instructions(self, recipe):
        self.instructions = sentence_extraction(get_information_from_df(
            recipe, INSTRUCTIONS_COLUMN)[0][INSTRUCTIONS_COLUMN])
        self.length = len(self.instructions)
        pass

    def read_instructions_stepwise(self):
        while True and self.context_instruction < self.length:
            instruction = self.instructions[self.context_instruction]
            self.socManager.emit_message(
                "voice_command_bot_response", instruction)
            engine_talk(instruction)

            question = "Should I move to next step or back? Else say break to exit"
            self.socManager.emit_message(
                "voice_command_bot_response", question)
            value = ask(question)

            if "back" in value and self.context_instruction > 0:
                self.socManager.emit_message("voice_command_bot_input", "Back")
                self.context_instruction -= 1
            elif "break" in value:
                self.socManager.emit_message(
                    "voice_command_bot_input", "Break")
                break
            elif "next" in value:
                self.socManager.emit_message("voice_command_bot_input", "Next")
                self.context_instruction += 1
            else:
                continue

    def read_ingredients_stepwise(self):
        while True and self.answer < len(self.ingredients):
            ingredient = self.ingredients[self.context_ingredient]
            self.socManager.emit_message(
                "voice_command_bot_response", ingredient)
            engine_talk(ingredient)

            question = "Should I move to next ingredient or back? Else say break to exit"
            self.socManager.emit_message(
                "voice_command_bot_response", question)
            value = ask(question)

            if "back" in value and self.context_ingredient > 0:
                self.socManager.emit_message("voice_command_bot_input", "Back")
                self.context_ingredient -= 1
            elif "break" in value:
                self.socManager.emit_message(
                    "voice_command_bot_input", "Break")
                break
            elif "next" in value:
                self.socManager.emit_message("voice_command_bot_input", "Next")
                self.context_ingredient += 1
            else:
                continue

    def increment(self):
        self.context += 1

    def decrement(self):
        self.context -= 1

    def get_context(self):
        return self.context

    def reset(self):
        self.context = 0

    def __str__(self):
        return self.recipe

    def __repr__(self):
        return self.recipe

    def get_ingredients(self):
        return self.ingredients

    def get_instructions(self):
        return self.instructions
