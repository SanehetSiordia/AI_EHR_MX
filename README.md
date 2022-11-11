# **Artificial Intelligence Electronic Health Record Mexico**
## Main Branch

This is the original version of my thesis project for my master's degree in *Bioingeniería  y Computo Inteligente”* of *“Centro Universitario de Ciencias Exactas e Ingenierías”* of the *“Universidad de Guadalajara”*.

4 different python programs were created for my thesis:
1.	Compilation, extraction, and storage of clinical notes and clinical laboratories data from PDFs in a database with MySQL (Branch: **PDFRecopilation**).
2.	Extraction and export in .csv files of data saved in the database for various analyzes during the master's degree, DOI:  [**10.24254/CNIB.21.56**](https://www.researchgate.net/publication/358785762_Identificacion_de_Variables_Clinicas_Asociadas_al_Diagnostico_Correcto_e_Incorrecto_en_Enfermedades_Respiratorias) (Branch: **SQLtoCSV**).
3.	Structured data analysis of clinical laboratories with decision trees algorithm (Branch: **DTanalysis**).
4.	Analysis of unstructured data from clinical notes with BiLSTM algorithm (Branch: **NLPanalysis**).

As a final product of this project the following article was published: **“Pneumonia and Pulmonary Thromboembolism Classification Using Electronic Health Records”** DOI: [**10.3390/diagnostics12102536**](https://doi.org/10.3390/diagnostics12102536)

![paper](README_images\paper.png "paper published.")

### **Program instruction**
>To use this program, you must download each branch of the repository on your local machine and follow the instructions specified in the README.md file of each branch.

### **Author's note**
>For external files (such as clinical notes or clinical laboratories in PDF format) it is required to be a collaborator and requests them via mail or message because they are files with sensitive information.

### **Future plans**
>The following has been proposed:
>1.	Homogenize the entire project in a single program.
>2.	Structure the project with the paradigm of object-oriented programming.
>3.	Sharing the original Database on a platform like Kaggle.
>4.	Use a GUI.
>5.	Transformers (*arXiv:1706.03762v5*) or other algorithms to power the project.
