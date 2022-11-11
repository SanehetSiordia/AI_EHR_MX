##  **PDFRecopilation Branch**

This section extracts data from 4 types of clinical records in PDF format:
1.	Clinical admission notes
2.	Medical consultation notes
3.	Discharge Clinical Notes
4.	Clinical Laboratory Results

These files are automatically renamed and organized in different folders from: *\AI_EHR_MX\DatosClinicos\6-Sin_Evaluar* with the use of regex and the *pdfplumber v0.7.5* package for read and extract the most relevant data from PDFs files. To organize the clinical discharge notes, the program reads the ICD10 codes that comes from the notes, and it is compared with those specified in the .txt file: *\AI_EHR_MX\TextFiles\CodigosCie10.txt*

The extracted data is saved in dictionaries and exported in .pickle files as a backup for not repeating the evaluation of existing files.

Finally, all the data stored in the .pickle files is exported to the database: *\AI_EHR_MX\mySQL_arch\enfermedadesresporatorias.sql* using SQL queries.

![Diagram](README_images\Diagram.png "Diagram of the relational model used.")
Figure 1. *Diagram of the relational model used*

**Author's note**

>For external files (such as clinical notes or clinical laboratories in PDF format) it is required to be a collaborator and requests them via mail or message because they are files with sensitive information.
