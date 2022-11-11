##  **Natural Language Processing Branch**

These section models the context of clinical interviews using Word Embedding and a BiLSTM network with Keras and Tensorflow packages.

The clinical interviews are imported from the database using SQL queries and a series of pre-processing is applied to adapt each word of each interview for the Word Embedding process:
1.	Tokenization
2.	Stop Words 
3.	Noise Removal 
4.	Capitalization 
5.	Stemming
6.	Lemmatization

This preprocessing is done with the help of the *NLTK v3.7.0* package.

### Text Preprocessing Code
```py
tokens = word_tokenize(text)

tokens = [w.lower() for w in tokens]

table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in tokens]

words = [word for word in stripped if word.isalpha()]

stop_words = set(stopwords.words('spanish'))
words = [w for w in words if not w in stop_words]

Snowball_stemmer = SnowballStemmer('spanish')
stemmed = [Snowball_stemmer.stem(word) for word in words]
```
After the text preprocessing, the *FastText v0.9.2* package is used to create Word Embeddings with the Biomedical Cased CBOW corpus from the study: [_**“Spanish Biomedical Word Embeddings in FastText”**_](https://zenodo.org/record/4543236)

![corpus](https://github.com/SanehetSiordia/AI_EHR_MX/tree/NLPanalysis/README_images/corpus.png) "corpus used")

Path to store the corpus: *\AI_EHR_MX\ModelBin*

The generated Word Embeddings are saved in .csv files (*\AI_EHR_MX\Archivos_CSV*) and in pickle files (*\AI_EHR_MX\PickleFiles*).

The parameters of the BiLSTM network were configured using the Grid Search method.

**Table 1.** *The original configuration of parameters.*
| Parameter | Value |
| ------ | ----------- |
| optimizer | SGD |
| learning rate | 0.1 |
| momentum | 0.1 |
| neurons | 50 |
| density | 1  |
| epoch  | 25  |

The BiLSTM model was evaluated with the metrics of Accuracy, Precision, Recall, F1 score, Cohens kappa and ROC AUC using the Sklearn package. The results are saved in .txt files in the path: *AI_EHR_MX\ResultsText*.

More information in the article **“Pneumonia and Pulmonary Thromboembolism Classification Using Electronic Health Records”** DOI: [_**10.3390/diagnostics12102536**_](https://doi.org/10.3390/diagnostics12102536)

![paper](https://github.com/SanehetSiordia/AI_EHR_MX/tree/NLPanalysis/README_images/paper.png) "paper published")
