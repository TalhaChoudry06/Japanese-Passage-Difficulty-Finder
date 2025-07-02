#Japanese Sentence Difficulty Classifier
This project is a machine learning-based application that classifies Japanese sentences by their JLPT (Japanese Language Proficiency Test) difficulty levels (N5 to N1). The application extracts linguistic features from input sentences, uses a trained classifier to estimate the difficulty, and displays detailed token analysis in a graphical user interface (GUI).

Features
Tokenizes Japanese sentences using a custom tokenizer

Extracts features like JLPT vocabulary counts and average JLPT level

Classifies sentences into JLPT difficulty levels using a trained machine learning model

Stores vocabulary and tags in an SQLite database for fast lookup

Provides a Tkinter-based GUI for user-friendly interaction

Saves and loads models and scalers using joblib for efficient deployment

Technologies & Libraries Used
Python 3

Tkinter (GUI)

SQLite (Database)

pandas, NumPy (Data processing)

scikit-learn (Machine learning)

joblib (Model persistence)

Installation
Clone this repository:

bash
Copy
Edit
git clone https://github.com/MangoMangoes245/Japanese-Passage-Difficulty-Finder.git
cd Japanese-Passage-Difficulty-Finder
Install required packages:

bash
Copy
Edit
pip install -r requirements.txt
Usage
To run the application, execute:

bash
Copy
Edit
python main.py
This will launch the GUI where you can input Japanese sentences and receive difficulty classification results with token analysis.

Project Structure
main.py — Entry point to launch the GUI application

scripts/feature_engineering.py — Tokenization and feature extraction logic

models/ — Serialized machine learning models and scalers (.joblib files)

database/ — SQLite database containing JLPT vocabulary and tags

Model Performance
The classifier achieves approximately 95% accuracy in predicting sentence difficulty levels, with precision, recall, and F1-scores above 90% across all JLPT levels.

License
MIT License

