"""
Simple Python Lambda service that uses response.json file in an S3 bucket to provide simple
responses to simple "fact"-like intents. The example response.json with this repo supports
the following:

Intents supported:

  Custom:
    About
    Contact
    Upcoming

  Required:
    LaunchRequest (request type)
    AMAZON.HelpIntent (intent)
    AMAZON.CancelIntent or AMAZON.StopIntent (intent, both use 'end' response)

Note, that as long as you keep your intents in sync with your skill intentSchema, you can
simply update or add intents to the JSON file in S3 and the lambda service will use them.
Intents in your Schema may be mixed case -- this code will convert to lower case.

Further note, there is .travis.yml in this repo that does two things:
  1) Deploys this code to your configured lambda function.
  2) Deploys the ../responses/response.json to your bucket.

If you fork this repo or create your own copy and keep it as a public repo, you can use
Travis to deploy to your lambda/S3. You'll want to change the following configs:

  in deploy-provider: lambda
    function_name
    role
    access_key_id (available from AWS console)
    secret_access_key (also available from AWS console, but make sure you use travis command
    line to encrypt your key)

  in deploy-provider: s3
    bucket (if you have changed it)
    access_key_id (can use the same one as above)
    secret_access_key (also use the same one as above)

"""

# If you want to use a different bucket name or response JSON file, change them here
BUCKET_NAME='alexa-python-biz'
RESPONSE_JSON='response.json'

import logging
import boto3
import json
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Load the S3 JSON
s3 = boto3.resource('s3')
# Grab the JSON from the file and load it into a map
json_string = s3.Object(BUCKET_NAME,RESPONSE_JSON).get()['Body'].read().decode('utf-8')
responses = json.loads(json_string)


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
    session_attributes = {} # No session attributes needed for simple fact responses
    reprompt_text = None # No reprompt text set
    speech_output = "<ssml>Unable to parse provided response file</ssml>"
    should_end_session = True # Can end session after fact is returned (no additional dialogue)

    if intent_name == 'launch':
        should_end_session = False # Opening a skill requires the session remain open
    elif intent_name == "AMAZON.HelpIntent":
        should_end_session = False # Asking for help requires the session remain open
        intent_name = 'help'
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        intent_name = 'end'
    else:
        intent_name = intent_name.lower()

    # Grab the response specified for the given intent in the JSON
    # The JSON may contain multiple responses for a single intent, further keyed
    # by some passed in parameter
    intent_resp = responses[intent_name]

    if isinstance(intent_resp,dict):
        try:
            intent_slot = intent['slots'][intent_name+'_slot']['value'].lower()
            speech_output = intent_resp[intent_slot]
        except:
            pass
    else:
        speech_output = responses[intent_name]

    return build_response(session_attributes, build_speechlet_response
                          (intent_name,speech_output,reprompt_text,should_end_session))


# --------------- Main handler ------------------

# This is the function called when the lambda is invoked by the skill.
# Essentially, JSON is passed in from ASK and your lambda must prepare the response JSON
#
def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    # Logging a message to CloudWatch to help with debugging once you are testing the lambda
    # and the skill that calls it.
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
    # allow the JSON to provide the response text for a LaunchRequest
    if event['request']['type'] == "LaunchRequest":
        event['request']['intent'] = { 'name':'launch' }
    
    return on_intent(event['request'], event['session'])

