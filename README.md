Perceptron
==========

Simple implementation of a perceptron that stores all data in a sqlite DB rather than in memory.

Currently writes to a sqlite database

Advantages
----------

- No need to retrain perceptron to create another model of it. Can simply load from db
- Can perform additional tasks on the computed/initial data set from db
- Data is standardised and easy to access
- Low memory use in training


Disadvantage
------------

- Higher training time due to I/O operations to DB


TODO
----
- Allow for MYSQL
