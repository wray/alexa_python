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


# --------------- Your functions to implement your intents ------------------

def about(intent, session):
    session_attributes = {}
    reprompt_text = None
    speech_output = ""
    should_end_session = False

    speech_output = "<speak>Welcome to ACME Inc. We are the coolest company located in the Silicon Valley of the South. We love our employees, customers, and the environment.</speak>"

    return build_response(session_attributes, build_speechlet_response
                          (intent['name'], speech_output, reprompt_text, should_end_session))

def contact(intent, session):
    session_attributes = {}
    reprompt_text = None
    speech_output = ""
    should_end_session = False

    speech_output = "<speak>The best way to reach us is at info at acme dot com. You can also leave us voice mail at 8 0 4, 5 5 5, 1 2 1 2. We are also on twitter, at acme S V O S.</speak>"

    return build_response(session_attributes, build_speechlet_response
                          (intent['name'], speech_output, remprompt_text, should_end_session))

def upcoming(intent, session):
    session_attributes = {}
    reprompt_text = None
    speech_output = ""
    should_end_session = False

    speech_output = "<speak>Check us out at Stir Trek dot com. We will have a booth and speakers in Columbus, Ohio on May  5th!</speak>"

    return build_response(session_attributes, build_speechlet_response
                          (intent['name'], speech_output, remprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for asking about our business. " \
      "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))




# --------------- Primary Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    logger.info("on_session_started requestId=" + session_started_request['requestId'] +
                ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    logger.info("on_launch requestId=" + launch_request['requestId'] +
                ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return build_response({},build_speechlet_response(
        "ACME Inc.", "<speak>Welcome to the 411 for ACME Inc. This skill provides information about ACME, a really cool company that Alexa loves to talk about.</speak>","",False))


def get_help():
    """ Called when the user asks for help
    """

    return build_response({},build_speechlet_response(
        "ACME Inc.","""<speak>This skill provides some basic information about ACME. You can ask for our location, contact info, and upcoming events.</speak>""","",False)) 


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    logger.info("on_intent requestId=" + intent_request['requestId'] +
                ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers

    if intent_name == "About":
        return about(intent, session)
    elif intent_name == "Contact":
        return contact(intent, session)
    elif intent_name == "Upcoming":
        return upcoming(intent,session)    
    elif intent_name == "AMAZON.HelpIntent":
        return get_help()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


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

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    else:
        return on_session_ended(event['request'], event['session'])
