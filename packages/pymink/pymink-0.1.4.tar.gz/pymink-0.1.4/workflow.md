# General Workflow Of tcat

tcat is a tool for processing text files and categorizing them into groups. For this purpose, a n-gram model is used to predict the input text's category.

## Input

- Inputs could be text files (maybe some other format, currently don't know).
- Future goal is for the input to be any article, but for now it's just text files. 
- All inputs have to be preprocessed as to be ready for the n-gram model. Preprocesing could be done by the user, or by tcat.
- The end goal is to have a database of n-grams of many categories, and then use the database to predict the category of the input.

## Preprocessing

- The input is preprocessed by removing all non-alphanumeric characters.
- All words are converted to UpperCase.

## N-Gram Model

- From the preprocessed input create a n-gram distribution. This is (currently) a dictionary of n-grams and their frequencies.
- This new model then calculates a distance between the input and each n-gram in the model.
- The distance could be through diferrent metrics that in the future could set by the user. For now, the distance is the calculated by simply adding the squares of the differences between the input's n-gram and the model's n-gram.

## Language Classifier and Category Classifier

For this project, the n-gram model is used to predict the category of the input. But before that, the input is classified into a language. 
Both of these classifications are done by the n-gram model.

# Output
The ouput should differ depending on which classifier is used. But in a general sense, the output should be a result object that
has the following attributes:

- `result.category` or `result.language`: The category of the input.
- `result.confidence`: The confidence of the result. This is a number between 0 and 1. and is calculated by the distance between the input and the n-gram.

and the following methods:

- `result.get_category()`: Returns the category of the input.
- `result.get_language()`: Returns the language of the input.
- `result.show_ngram()`: Prints the n-gram of the input.