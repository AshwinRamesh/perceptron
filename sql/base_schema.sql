-- This file describes the basic schema of the database created and used by the perceptron model implemented.

/* perceptron_details: stores all auxilary details about a perceptron */
CREATE TABLE perceptron_details (
    id INTEGER PRIMARY KEY,
    iteratations INTEGER
)

/* classes: stores all classes that can be classified for the model */
CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    class TEXT
);

/* features: stores all features of each data item in the perceptron model */
CREATE TABLE features (
    id INTEGER PRIMARY KEY,
    feature TEXT
);

/* training_datas: each row stores a training data item */
CREATE TABLE training_datas (
    id INTEGER PRIMARY KEY,
    class INTEGER,
    feature_1 REAL,
    feature_2 REAL,
    ... -- each feature name is a column name in this table
);

/* weights: stores the current weights of each class */
CREATE TABLE weights (
    id INTEGER PRIMARY KEY,
    class INTEGER, -- foreign key to classes table
    feature_1 REAL,
    feature_2 REAL,
    ..  -- each feature name is a weight column in this table
);

/* historical_weights: stores the histoical changing weights as the model is trained */
CREATE TABLE historical_weights (
    id INTEGER PRIMARY KEY,
    class INTEGER, -- foreign key to classes table
    feature_1 REAL,
    feature_2 REAL,
    ..  -- each feature name is a weight column in this table
);

/* classification_data: stores the data that is being classified */
CREATE TABLE classification_data (
    id INTEGER PRIMARY KEY,
    classified_class INTEGER, -- foreign key to classes
    feature_1 REAL,
    feature_2 REAL,
    ... -- each feature name is a weight column in this table
);
