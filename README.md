# Build an Alexa Skill using basic Python functions

## Review the presentation to learn more about Alexa and the Cloud:
[Intro to Alexa](https://github.com/full-steam-ahead/alexa/blob/master/Create%20Your%20First%20Alexa%20Skill.pdf)  

Note: In order for the presentation's hyperlinks to work, you must click the Download button and open the PDF. 

## What You Will Learn

This repo contains a simple python example that implements a basic "My
School Info" Skill

* Introduction to building an Alexa Skill without getting too much
into code.
* Voice User Interface (VUI) design
* SSML
* Lambda Services
* Simple Python functions

## What You Will Need

* [Amazon Developer Portal Account](http://developer.amazon.com)
* [Amazon Web Services Account](http://aws.amazon.com/)
* The sample code on [GitHub](https://github.com/full-steam-ahead/alexa).

## What Your Skill Will Do

An Alexa skill built using a lambda function built with Python that
translates an intent to a function call. Implement custom intents by
simply updating or creating a function to return the SSML for Alexa to speak.

Suppose you name your skill My School, you will be able to interact
with your skill with phrases like, "Alexa, ask My School for contact
info" or "Alexa, ask My School for upcoming events." or "Alexa,
ask My School for general info." or "Alexa, tell me about
My School."

## Make it Your Own

Just create a new Alexa Skill Kit skill on [developer.amazon.com](https://developer.amazon.com) named after your school (both skill name and invocation name). Then copy and paste the
intentSchema and Utterances into the Skill builder. On, [aws.amazon.com](https://aws.amaxon.com) you can then create the
lambda and copy the code in alexa_py.py into the lambda function.

Then update the responses in the functions at the top
of the file and re-test your skill to provide relevant information for your school.

But, wait, that's not all. Go ahead and completely change the skill to
a different set of information for another school or organization. Or change your
invocation to "my school facts" and create different/new intents and
utterances for RandomFacts, AcademicFacts, SportsFacts, etc. And then you'll
soon be ready to start using parameters to make things even more
dynamic.

So, as long as you keep your intents in sync: skill intent schema & utterences, lambda functions; you can
simply update or add intents matching intent name to function name (lowercase) and your skill will respond with your updated or new response.

Note, Intents in your Schema may be mixed case -- the python lambda code will convert to lower case.



