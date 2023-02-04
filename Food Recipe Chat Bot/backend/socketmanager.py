class SocManager():
    def __init__(self):
        self.recipe_selected = False

    def get_recipe_selection_status(self):
        return self.recipe_selected

    def set_socket(self, socket):
        self.socketio = socket

    def set_recipes_df(self, recipe_df):
        self.recipe_df = recipe_df
        self.all_recipes = recipe_df.to_dict('records')

    def set_recipes(self, recipe):
        self.recipes = recipe

    def get_recipes(self):
        return self.all_recipes

    def set_question(self, question):
        self.question = question

    def get_question(self):
        return self.question

    def set_recipe(self, recipe):
        self.recipe = recipe
        self.recipe_selected = True

    def get_recipe(self):
        return self.recipe

    def emit_message(self, event, message):
        self.socketio.emit(event, message)

    def emit_data(self, event, message):
        self.socketio.emit(event, {'data': message})