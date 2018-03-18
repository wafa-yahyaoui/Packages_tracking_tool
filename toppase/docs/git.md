# git-flow #

This document would normally document whatever steps are necessary to work with git-flow.

### Initialize ###
Start using git-flow by initializing it inside an existing git repository:
* git flow init

You'll have to answer a few questions regarding the naming conventions for your branches.
It's recommended to use the default values.


### Start a new feature ###

* git flow feature start MYFEATURE


### Finish up a feature ###

* git flow feature finish MYFEATURE

Finish the development of a feature. This action performs the following:

* Merges MYFEATURE into 'develop'
* Removes the feature branch
* Switches back to 'develop' branch

### Publish a feature ###

* git flow feature publish MYFEATURE

### Getting a published feature ###

* git flow feature pull origin MYFEATURE


### Start a release ###

* git flow release start RELEASE [BASE]

### publish a release  ###

* git flow release publish RELEASE

### Finish up a release ###

* git flow release finish RELEASE

Finishing a release is one of the big steps in git branching. It performs several actions:

* Merges the release branch back into 'master'
* Tags the release with its name
* Back-merges the release into 'develop'
* Removes the release branch
* Don't forget to push your tags with git push --tags


### Start a hotfix ###

* git flow hotfix start VERSION [BASENAME]

### Finish a hotfix ###

* git flow hotfix finish VERSION
