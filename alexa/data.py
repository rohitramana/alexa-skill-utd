# -*- coding: utf-8 -*-

# Resolving gettext as _ for module loading.
from gettext import gettext as _

SKILL_NAME = _("coursebook")
WELCOME_MESSAGE = _("Welcome to {}. You can ask a question like, tell me about machine learning? ... Now, what can I help you with?")
WELCOME_REPROMPT = _("For instructions on what you can say, please say help me.")
DISPLAY_CARD_TITLE = _("{}  - Recipe for {}.")
HELP_MESSAGE = _("You can ask questions such as, You can ask a question like, tell me about machine learning?, or, you can say exit...Now, what can I help you with?")
HELP_REPROMPT = _("You can say things like, what courses are offered by a particular professor, or you can say exit...Now, what can I help you with?")
FALLBACK_MESSAGE = _("The {} skill can't help you with that.")
STOP_MESSAGE = _("Goodbye!")
RECIPE_REPEAT_MESSAGE = _("Try saying repeat.")
RECIPE_NOT_FOUND_MESSAGE = _("I'm sorry, I currently do not know ")
RECIPE_NOT_FOUND_WITH_ITEM_NAME = _("the recipe for {}. ")
RECIPE_NOT_FOUND_WITHOUT_ITEM_NAME = _("that recipe. ")
RECIPE_NOT_FOUND_REPROMPT = _("What else can I help with?")

