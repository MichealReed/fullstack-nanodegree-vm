rdb-fullstack
=============

Common code for the Relational Databases and Full Stack Fundamentals courses

This program allows you to register any even number of players, and using a swiss pairing technique, pair them together related to their win record.

## Getting Started:

* Navigate to the included Vagrant folder in your favorite shell, and run "vagrant up" - this step can take some time while the system sets up all necessary files.
* Next, run vagrant SSH to access our newly created virtual machine.


## Adding Our Database:

* Navigate to the tournament folder by typing "cd /vagrant/tournament
* In the vagrant command line, type "psql -f tournament.sql" to create out database.

## Running Our Program:

* Now you can create a new python file specific to your tournament and start pairing!
* Reference the tournament_test.py file to understand how to register, pair players, and report matches
* You can run the tournament_test.py or yourfile.py by typing "python tournament_test.py" in the vagrant shell - NOTE: You must be in the tournament directory

