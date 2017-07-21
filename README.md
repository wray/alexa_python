# Build an Alexa Skill using basic Python functions

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

Suppose you name your skill My Skill., you will be able to interact
with your skill with phrases like, "Alexa, ask My School for contact
info" or "Alexa, ask My School for upcoming events." or "Alexa,
ask My School for general info." or "Alexa, tell me about
My School."

## Make it Your Own

By simply copying and pasting the
intentSchema and Utterances into the Skill builder, you can create the
lambda and copy the code in alexa_py into the lambda function.

You can then easily update the responses in the functions at the top
of the  file and re-test your skill.

Update the invocation name to a different school and match your
response to provide relevant information for the school.

But, wait, that's not all. Go ahead and completely change the skill to
a different set of information for another school or organization. Change your
invocation to pet facts and create different/new intents and
utterances to for randomFacts, furCare, etc. And then you'll
quickly be ready to start using parameters to make things even more
dynamic.

So, as long as you keep your JSON intents in sync with your skill intentSchema, you can
simply update or add intents as functions and the lambda service will use them.
Intents in your Schema may be mixed case -- this code will convert to lower case.



