# Movie Dialogue Classifier
Multi-label natural language processing (NLP) classification model to predict movies' genres from dialogue.

### Table of Contents

1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [Data Preprocessing and Modelling](#model)
4. [File Descriptions](#files)
5. [Licensing, Authors, and Acknowledgements](#licensing)

## Installation <a name="installation"></a>

There should be no necessary libraries to run the code here beyond the Anaconda distribution of Python. The code should run with no issues using Python version 3.

## Project Motivation<a name="motivation"></a>

The motivation behind undertaking this project was to explore whether text patterns could be uncovered in movies' dialogue to act as indicators of their genres. The steps of the process were as follows:

1. Extracting and transforming the raw data contained within the source files and loading to a SQLite database
2. Exploring the training data to uncover evidence of class and label imbalances
3. Implementing NLP techniques to convert raw text data into a matrix of feature variables
4. Building and tuning a classification model to produce a multi-output genre prediction when passed a text quote

A more in-depth discussion of the process of building the model can be found in a Medium post linked [here]().

## Data Preprocessing and Modelling<a name="model"></a>

The data for this project was obtained via a publication from Cornell University (see acknowledgements below).

Of the files provided, there were three dataframes of interest to this project: `movie_conversations`, `movie_lines`, and `movie_titles_metadata`. The steps taken to extract the necessary data and transform it into a format suitable for the project were as follows:

1. Read the data from each of the three `.txt` files into pandas dataframes
2. Assign a conversation ID to each exchange contained in the conversations dataframe
3. Melt the conversations dataframe such that each utterance appears on a separte row with the corresponding conversation ID
4. Join the melted dataframe with the lines dataframe to retrieve the actual text for each line ID
5. Join the separate rows via the conversation ID such that the entirety of each exchange appears in text format on an individual row
6. Finally, join the dataframe of text conversations with the movie metadata to retrieve the genres for each text document, and load the final dataframe to a SQLite database

A more complete description of the raw data files can be found in a README within the corpus folder in the repository, as provided by the publication.

Once the raw data had been transformed into a workable format, the steps for processing the data into a model-friendly representation were as follows:

1. Remove all punctuation and special characters from the text using a regular expression
2. Tokenise each document in the text
3. Lemmatise tokens, set to lower case, strip whitespace and filter out stop words
4. Convert documents into a matrix of vectorised token counts
5. Transform matrix into tf-idf representation

This process rendered the exchanges into a matrix of fearures suitable to train a Decision Tree Classification model, with the 24 genres acting as a multi-label target variable.

The NLP preprocessing and model fitting were bundled into a single pipeline to prevent data leakage and render the model selection and hyper-parameter tuning processes more efficient.

## File Descriptions <a name="files"></a>

- `cornell_movie_dialogs_corpus`: folder containing raw source data files
- `movie_dialogue_etl.py`: Python program to extract and transform raw data and load to a local SQLite database
- `dialogue.db`: SQLite database containing training data set
- `movie_dialogue_clf.ipynb`: notebook used to construct classification model

## Licensing, Authors, Acknowledgements <a name="licensing"></a>

The data for this project was obtained courtesy of the publication [Cornell Movie--Dialogs Corpus](https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html) from Cristian Danescu-Niculescu-Mizil at Cornell University.
