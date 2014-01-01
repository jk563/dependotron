dependotron
===========

Dependency finding by crawling repo pom files.


Background and Aim
------------------

Depend-o-tron is intended to be set of tools to help understand dependencies between Maven components. The principle aim can be understood be understanding this scenario:

    Given a shared Java component, when I want to update the shared component, then what might be affected by my changes?

Maven and artifactory have good support for showing what components are depended *upon*, but not for what components *dependent*.


Technique
---------

Depend-o-tron has a data harvester and a front-end component. The harvester collects data about dependencies and stores them in a database. The front-end uses the data in the database to display information to the user.
