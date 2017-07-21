"""
Simple Python Lambda service that provides simple responses to simple "fact"-like intents.
This file supports the following:

Intents supported:

  Custom:
    About
    Contact
    Upcoming

  Required:
    LaunchRequest (request type that calls launch function)
    AMAZON.HelpIntent (intent that calls help function)
    AMAZON.CancelIntent or AMAZON.StopIntent (intent, both use end function)

Note, that as long as you keep your intents are in sync with your skill intentSchema, you can
simply update or add intents as functions here and the lambda service will use them.
Intents in your Schema may be mixed case -- this code will convert to lower case.


"""

import sys
import re
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)



import logging

# **************************** CUSTOMIZE BELOW *************************************************

# --------------- Your functions that implement your intents ------------------

def about():
    return "<speak>Welcome to My School. We are the coolest school located in the Silicon Valley of the South. We love our students, staff, teachers and the community.</speak>"

def contact():
    return "<speak>The best way to reach us is at info at my school dot E D U. You can also leave us voice mail at 8 0 4, 5 5 5, 1 2 1 2. We are also on twitter, at my school.</speak>"

def upcoming():
    return "<speak>The Full Steam Ahead is Friday, July twenty first.</speak>"


# --------------- Primary/Required functions (update as needed) ------------------

def launch():
    """ Called when the user launches the skill without specifying what they want
    """

    return "<speak>Welcome to the 4 1 1 for my school. This skill provides information about my school, a really cool school located in the Silicon Valley of the South. You can ask for general info, contact info, and upcoming events.</speak>"


def help():
    """ Called when the user asks for help
    """

    return "<speak>This skill provides some basic information about my school. You can ask about us, contact info, and upcoming events.</speak>"


def end():

    return "<speak.Thank you for asking about my school. Have a nice day! </speak>"


# ***************************** CUSTOMIZE ABOVE **************************************************

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):

    card_output = re.sub('<[^>]*>', '', output)
    
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': card_output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# Function which delegates the speech output for the response based on the JSON file.
# Simply looking up the intent in the responses map created from the parsed JSON.
#
def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    logger.info("on_intent requestId=" + intent_request['requestId'] +
                ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    session_attributes = {} # No session attributes needed for simple fact response
    reprompt_text = None # No reprompt text set
    speech_output = ""
    should_end_session = True # Can end session after fact is returned (no additional dialogue)

    if intent_name == "launch":
        should_end_session = False # Opening a skill requires the session remain open
    elif intent_name == "AMAZON.HelpIntent":
        should_end_session = False # Asking for help requires the session remain open
        intent_name = 'help'
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        intent_name = 'end'
    else:
        intent_name = intent_name.lower()

    # Grab the response specified for the given intent of the JSON by calling
    # the function defined in my_py
    speech_output = getattr(sys.modules[__name__], intent_name)()

    return build_response(session_attributes, build_speechlet_response
                          (intent_name,speech_output,reprompt_text,should_end_session))

# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    logger.info("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    # I am injecting a new "intent" type of launch in order to
    # allow my_py to provide the response text for a LaunchRequest
    if event['request']['type'] == "LaunchRequest":
        event['request']['intent'] = { 'name':'launch' }
    
    return on_intent(event['request'], event['session'])

