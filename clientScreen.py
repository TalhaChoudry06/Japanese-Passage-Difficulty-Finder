import tkinter as tk
from scripts.feature_engineering import tokenizer  # Your custom tokenizer module
import sqlite3
import joblib
import pandas as pd

classifier = joblib.load("classifier/predicted_sentences_classifier.joblib")
scaler = joblib.load("classifier/predicted_sentences_scaler.joblib")
conn = sqlite3.connect('database/words.db')
cursor = conn.cursor()

# This is the pop-up window that appears when you click "Analyse"
class Window(tk.Toplevel):
    def __init__(self, parent, input_sentence):
        super().__init__(parent)

        self.geometry('400x300')
        self.title('Japanese Sentence Analysis')

        # Tokenize input
        sentence_tokens = tokenizer.tokenize(input_sentence)

        # JLPT counters
        n5 = n4 = n3 = n2 = n1 = 0

        # Display token analysis
        output_text = tk.Text(self, height=15, width=50)
        output_text.pack(padx=10, pady=10)

        for token in sentence_tokens:
            cursor.execute("SELECT tags FROM words WHERE expression = ? LIMIT 1", (token,))
            result = cursor.fetchone()

            if result:
                tag = result[0].lower()  # e.g., 'n5'
                if tag == 'n5': n5 += 1
                elif tag == 'n4': n4 += 1
                elif tag == 'n3': n3 += 1
                elif tag == 'n2': n2 += 1
                elif tag == 'n1': n1 += 1

            # Display token info
            surface = getattr(token, 'surface', str(token))
            base = getattr(token, 'base_form', surface)
            output_text.insert(tk.END, f"{surface}\n")

        tokens = len(sentence_tokens)

        # Compute average JLPT (inverted scale: N5 is 1, N1 is 5)
        total = n1 + n2 + n3 + n4 + n5
        if total > 0:
            avg_jlpt = (n5 * 1 + n4 * 2 + n3 * 3 + n2 * 4 + n1 * 5) / total
        else:
            avg_jlpt = 5  # Assume hardest if unknown

        # Now build feature vector in correct order
        raw_features = [n5, n4, n3, n2, n1, tokens, avg_jlpt]
        feature_names = ['n5', 'n4', 'n3', 'n2', 'n1', 'tokens', 'avg_jlpt']
        input_df = pd.DataFrame([raw_features], columns=feature_names)

        # Scale features
        scaled_features = scaler.transform(input_df)

        # Predict JLPT level
        prediction = classifier.predict(scaled_features)

        # Show prediction in window
        output_text.insert(tk.END, f"\nPredicted Sentence Level: {prediction[0]}\n")
        output_text.configure(state='disabled')

        # Close button
        tk.Button(self, text='Close', command=self.destroy).pack(pady=5)

        # Make popup modal
        self.grab_set()


# This is the main app window where the user inputs a sentence
class App(tk.Tk):
    def __init__(self):
        super().__init__()  # Initialize the Tk window

        self.geometry('400x200')  # Set size of main window
        self.title('Japanese Sentence Analyser')  # Set title

        # Label above the input box
        tk.Label(self, text="Enter a Japanese sentence:").pack(pady=(10, 0))

        # Multiline text input box for the user to enter the sentence
        self.text_box = tk.Text(self, height=4, width=40)
        self.text_box.pack(padx=10, pady=10)

        # Button to submit the sentence for analysis
        tk.Button(self, text='Analyse', command=self.retrieve_input).pack()

    # This function is called when "Analyse" is clicked
    def retrieve_input(self):
        # Get text from the input box, remove leading/trailing whitespace
        input_value = self.text_box.get("1.0", "end-1c").strip()
        if input_value:  # If not empty
            self.open_window(input_value)  # Open the output window with analysis

    # Opens the output window (defined above) with the input sentence
    def open_window(self, sentence):
        Window(self, sentence)


# This block ensures the app only runs when this file is executed directly
if __name__ == "__main__":
    app = App()      # Create an instance of the App
    app.mainloop()   # Start the Tkinter event loop
