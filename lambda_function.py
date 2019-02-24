# -*- coding: utf-8 -*-

# HowTo skill: A simple skill that shows how to use python's
# gettext module for localization, for multiple locales.

import logging
import gettext

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractResponseInterceptor, AbstractRequestInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

from alexa import data, util
import pandas as pd

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

coursebookData = pd.read_csv("coursebook.csv",parse_dates = ["StartTime", "EndTime", "StartDate", "EndDate"])
def isStringAvailable(string):
	return string!=None and len(string)!=0

class LaunchRequestHandler(AbstractRequestHandler):
	"""Handler for skill launch."""
	def can_handle(self, handler_input):
		# type: (HandlerInput) -> bool
		return is_request_type("LaunchRequest")(handler_input)

	def handle(self, handler_input):
		# type: (HandlerInput) -> Response
		logger.info("In LaunchRequestHandler")
		_ = handler_input.attributes_manager.request_attributes["_"]

		locale = handler_input.request_envelope.request.locale
		speech = _(data.WELCOME_MESSAGE).format(
			_(data.SKILL_NAME))
		reprompt = _(data.WELCOME_REPROMPT)

		handler_input.response_builder.speak(speech).ask(reprompt)
		return handler_input.response_builder.response




class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        locale = handler_input.request_envelope.request.locale
        

        speech = _(data.HELP_MESSAGE)

        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


class RepeatIntentHandler(AbstractRequestHandler):
    """Handler for Repeat Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In RepeatIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        session_attributes = handler_input.attributes_manager.session_attributes
        handler_input.response_builder.speak(
            session_attributes['speech']).ask(
            session_attributes['reprompt'])
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Handler for Cancel and Stop Intents."""
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        speech = _(data.STOP_MESSAGE).format(_(data.SKILL_NAME))
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.

    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        locale = handler_input.request_envelope.request.locale

        help_message = _(data.HELP_MESSAGE)
        help_reprompt = _(data.HELP_REPROMPT)
        speech = _(data.FALLBACK_MESSAGE).format(
            _(data.SKILL_NAME)) + help_message
        reprompt = _(data.FALLBACK_MESSAGE).format(
            _(data.SKILL_NAME)) + help_reprompt

        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for SessionEndedRequest."""
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")
        logger.info("Session ended with reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Global exception handler."""
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        _ = handler_input.attributes_manager.request_attributes["_"]
        logger.error(exception, exc_info=True)
        logger.info("Original request was {}".format(
            handler_input.request_envelope.request))

        speech = _("Sorry, I can't understand the command. Please say again!!")
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


class CacheSpeechForRepeatInterceptor(AbstractResponseInterceptor):
    """Cache the output speech and reprompt to session attributes,
    for repeat intent.
    """
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["speech"] = response.output_speech
        session_attr["reprompt"] = response.reprompt


class LocalizationInterceptor(AbstractRequestInterceptor):
    """Add function to request attributes, that can load locale specific data."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))
        i18n = gettext.translation(
            'data', localedir='locales', languages=[locale], fallback=True)
        handler_input.attributes_manager.request_attributes[
            "_"] = i18n.gettext


        
class CourseBasicsIntentHandler(AbstractRequestHandler):
	"""Handler for Cancel and Stop Intents."""
	def can_handle(self, handler_input):
		return (is_intent_name("CourseBasicsIntent")(handler_input))

	def handle(self, handler_input):
		# type: (HandlerInput) -> Response
		logger.info("In CourseBasicsIntentHandler")


		_ = handler_input.attributes_manager.request_attributes["_"]
		courseName = handler_input.request_envelope.request.intent.slots["CourseName"].value
		result = None
		speech = "There are no courses available"
		if(isStringAvailable(courseName)):
			result = coursebookData[coursebookData["ClassTitle"].str.lower().str.contains(courseName.lower())]			
			if(len(result)>0):
				speech = ""
				if(len(result)>1):
					speech = "There are " + str(len(result)) + " courses available."
					speech = speech + " Top result is "
				
				topResult = result.to_dict("records")[0]			
				speech = speech +  topResult["ClassTitle"] + " offered by " + topResult["Instructor"] + ". It is a " + topResult["InstructionMode"] + " " + topResult["ActivityType"] + " class on "+ topResult["Days"] + " from " + topResult["StartTime"].strftime("%I %M %p") + " to " + topResult["EndTime"].strftime("%I %M %p") + " starting from " + topResult["StartDate"].strftime("%b %d, %Y") + " and ending on "+ topResult["EndDate"].strftime("%b %d, %Y")
				speech = speech.replace("&","and")
		handler_input.response_builder.speak(speech)
		return handler_input.response_builder.response
		
class ProfessorIntentHandler(AbstractRequestHandler):
	"""Handler for Cancel and Stop Intents."""
	def can_handle(self, handler_input):
		return (is_intent_name("ProfessorIntent")(handler_input))

	def handle(self, handler_input):
		# type: (HandlerInput) -> Response
		logger.info("In ProfessorIntentHandler")


		_ = handler_input.attributes_manager.request_attributes["_"]
		courseName = handler_input.request_envelope.request.intent.slots["CourseName"].value
		instructorName = handler_input.request_envelope.request.intent.slots["ProfessorName"].value
		result = None
		speech = "This course is not available"
		if(isStringAvailable(courseName)):
			result = coursebookData[coursebookData["ClassTitle"].str.lower().str.contains(courseName.lower())]			
			if(len(result)>0):
				result = set(result["Instructor"].tolist())
				speech = "Professor "+",Professor ".join(result)
		elif(isStringAvailable(instructorName)):
			result = coursebookData[coursebookData["Instructor"].str.lower().str.contains(instructorName.lower())]			
			if(len(result)>0):
				result = set(result["ClassTitle"].tolist())
				speech = ",".join(result)
			
				
		handler_input.response_builder.speak(speech)
		return handler_input.response_builder.response

class CourseEnrollmentIntentHandler(AbstractRequestHandler):
	"""Handler for Cancel and Stop Intents."""
	def can_handle(self, handler_input):
		return (is_intent_name("CourseEnrollmentIntent")(handler_input))

	def handle(self, handler_input):
		# type: (HandlerInput) -> Response
		logger.info(CourseEnrollmentIntentHandler)


		_ = handler_input.attributes_manager.request_attributes["_"]
		courseName = handler_input.request_envelope.request.intent.slots["CourseName"].value
		result = None
		speech = "course is not available"
		if isStringAvailable(courseName):
			courseId = courseName.split(".")[0]
			courseSection = courseName.split(".")[1]
			speech = "You cannot enroll as course is closed"
			result = coursebookData[coursebookData["CourseID"].str.contains(courseId, case=False) & coursebookData["Section"].str.contains(courseSection, case=False) & coursebookData["Status"].str.contains("open", case=False)]

			if len(result) > 0:
				speech = "You cannot enroll as you require department or professor's consent"   
				consent = result["Consent"].str.contains('y', case=False).iloc[0]
				if(consent==False):
					prereq = result["Prerequisites"]
					speech = ""
					if(prereq is None):
						speech = "You have prereqs for this course. Please make sure you complete them before enrolling"
					else:
						speech = "You dont have any prereqs for this course. You are free to enroll."
						availableSeats = result["Available Seats"].iloc[0]
						if availableSeats < 5:
							speech = speech + " Seats are fast filling. There are less than 5 seats available"
						else:
							speech = speech + " You have " + str(availableSeats) + " seats left"
			
				
		handler_input.response_builder.speak(speech)
		return handler_input.response_builder.response
		

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(RepeatIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(CourseBasicsIntentHandler())
sb.add_request_handler(ProfessorIntentHandler())
sb.add_request_handler(CourseEnrollmentIntentHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())
sb.add_global_response_interceptor(CacheSpeechForRepeatInterceptor())

lambda_handler = sb.lambda_handler()
