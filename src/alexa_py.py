"""
Simple Python Lambda service providing example for a small business "voice site". You know,
this is like the Alexa version of your web site.

Intents supported:
  Amazon.HelpIntent
  About
  Contact
  Upcoming


"""

import logging
import my_py

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
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


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    logger.info("on_intent requestId=" + intent_request['requestId'] +
                ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers

    session_attributes = {}
    reprompt_text = None
    speech_output = ""
    should_end_session = True

    if intent_name == "AMAZON.HelpIntent":
        should_end_session = False
        speech_output = help()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        speech_output = end()
    else:
        intent_name = intent_name.lower()
        speech_output = getattr(my_py,intent_name)()

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

    if event['request']['type'] == "LaunchRequest":
        event['request']['intent']['name'] = 'launch'
    
    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    else:
        return help()
