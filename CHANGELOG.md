# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

##  [1.1]
###  Added
- A real and dynamic mongodb repository to modify the model.

###  Fixed
- Bug of logging twice

##  [1.0]
###  Changed
- Modified the architecture to have a more robust server.

###  Removed
- No data folder is needed anymore. Load of model nlp is done on start

##  [0.1]
###  Added
- Added some response fields : ``verbs``, ``lemmas``, ``tokens``
- Created ``TRIGGER_SHOPPING_LIST`` intent
- Created a Dockerfile to generate a docker image
- Initialized the main architecture
- Initialized the helm folder for automatic deployments
