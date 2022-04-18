DBD Load Times
==============

This python script checks for the dbd window loading, if it finds it in a 
loading state it will wait for the loading to finish and record the time
it took to load.
You then can input the map name, and it will save the time to a file while
printing out the average.

Usage
--------
Start the program up, it will then detect the DBD window.
If it finds it everything will start automatically.
If it finds a loading screen it'll start recording the changes until it's out of loading.
Do not tab out of the window, it has to stay visible.

How does it work?
----------------

It externally takes a screenshot of the DBD window and then uses the PIL library to
detect black pixels.

Planned features
----------------
It is planned to automatically detect the map played based upon the 
gray map name displayed on the bottom left when loading in.