Rice University | COMP 413 | Mobile Team #1 | Fall 2021

# What is VizBuzz? 
VizBuzz is a mobile app that brings the intricacies and nuances of audio podcasts to those who are deaf or hard of hearing. By providing a real time, enhanced transcription system, users can glean insight into auditory subtleties via visual cues. For example, a positive sentiment can be indicated by green text, whereas a negative phrase can be illustrated with red. VizBuzz provides a way for users to upload any podcast they wish, then have the option to play it back alongside the enhanced transcript. 

## Features
* Intelligent transcription service via Microsoft Azure's Cognitive Services API
* Cross-platform frontend built in ReactNative
* Customizable podcast library with support for users to upload podcasts
* Visual cues for sentiment, pitch, and volume
* Secure user authentication and accounts system
* Robust backend in Azure, Django, AWS, and Heroku

## How to run
\[TBD\]

## Files explained
This repository contains the code for the backend.
* `.github/workflows`
  * The script for running Github Actions. Every time a commit is made, Actions builds our projects, executes unit tests, and computes the code coverage.
* `BackendConfig/API`
  * `/Transcriber` converts and streams an audio file, calling the Microsoft API and generating the transcript.
  * `/views` holds the endpoints to the Django server.
  * `test.py` contains the unit tests for the backend.
* `BackendConfig/BackendConfig`
  * Contains necessary configurations for Django.

## Team
VizBuzz is created with ♥️ by Prashanth Pai, Grace Nichols, Michael Sprintson, Timothy Goh, Colin King, Lucas Banus, and Rashi Bose.

## Relevant links
* [Frontend repo](https://github.com/lucasbanus/VizBuzzReactNative)
* [Final presentation](https://www.canva.com/design/DAEx5DlQ8yQ/yLGnvcUL5SakNDOrkQZE0w/view?utm_content=DAEx5DlQ8yQ&utm_campaign=designshare&utm_medium=link&utm_source=sharebutton)
