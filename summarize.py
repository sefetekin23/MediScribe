from speech_rec import take_input
from flask import Flask, jsonify
from flask_cors import CORS
def extract_health_info(text: str):
    # lists of keywords for each category
    symptoms_keywords = [
        'pain', 'fatigue', 'fever', 'headache', 'nausea', 'vomiting',
        'diarrhea', 'dizziness', 'breathing', 'breathless', 'cough',
        'sore throat', 'muscle aches', 'swelling', 'bruising',
        'rash', 'itching'
    ]

    med_keywords = [
        'paracetamol', 'ibuprofen', 'aspirin', 'antibiotic', 'antidepressant',
        'antipsychotic', 'antihistamine', 'vaccine', 'immunotherapy', 'chemotherapy',
        'painkiller', 'analgesic', 'antidepressant', 'antipsychotic',
        'antihistamine', 'vaccine', 'immunotherapy', 'chemotherapy',
        'radiation', 'surgery', 'transplant', 'dialysis', 'ventilator',
        'anesthesia', 'insulin', 'steroid', 'physical therapy',
        'psychotherapy', 'chiropractic', 'acupuncture', 'homeopathy',
        'hormone therapy', 'antiviral', 'antifungal', 'anticoagulant',
        'statin', 'ACE inhibitor', 'aspirin', 'metformin', 'physical'
    ]
    
    diagnosis_keywords = [
        'respiratory infection', 'pneumonia', 'bronchitis', 'asthma', 'COPD',
        'lung cancer', 'COVID-19', 'coronavirus', 'influenza', 'flu',
        'common cold', 'sinusitis', 'hay fever', 'pulmonary fibrosis', 
        'tuberculosis', 'TB', 'lung abscess', 'pleurisy', 'pleural effusion',
        'cystic fibrosis', 'pulmonary edema', 'pulmonary nodules',
        'cancer', 'tumor', 'virus', 'bacteria', 'inflammation'
    ] 
    
    # Define phrases that typically indicate a recommendation or a statement of current medication
    rec_phrases = ["i recommend", "you should", "try taking"]
    cur_phrases = ["i am taking", "i have been prescribed", "my current medication is"]

    rec_med = []
    cur_med = []

    # Convert the text to lowercase and split into words
    text = text.lower()
    words = text.split()

    # Iterate over the words
    for i, word in enumerate(words):
        # If the word is a med keyword, check if the previous word was a rec phrase or a cur phrase
        if word in med_keywords:
            # Get the previous 5 words
            prev_text = ' '.join(words[max(0, i-5):i]) 

            # If a rec_phrase is in previous text, add the current word to rec_med
            if any(phrase in prev_text for phrase in rec_phrases):
                rec_med.append(word)
            # If a cur_phrase phrase is in the previous text, add the current word to cur_med
            elif any(phrase in prev_text for phrase in cur_phrases):
                cur_med.append(word)

    # Extract words that match the keywords for each category
    symptoms = [word for word in symptoms_keywords if word in text]
    diagnosis = [word for word in diagnosis_keywords if word in text]

    return list(set(symptoms)), list(set(rec_med)), list(set(cur_med)), list(set(diagnosis))



# Example text
example_conversation = '''Hello, Doctor.
Before we start, this appointment is being recorded and the audio will be deleted after the session.
It’s used to fill out your patient information. Is that okay with you? 
Yeah, fine by me. 
So how are you, what seems to be the issue? 
I have had a cough for the past week. 
Okay, can you tell me more about your cough? 
It’s kind of chesty and i feel breathless when it happens. 
Okay, are you currently taking any medication? 
Yeah, i am taking paracetamol . 
Alright, having heard your symptoms it’s possible you have a respiratory infection. 
We can run some tests, and you should do a physical exam. 
Alright, thank you for your help.'''

#Run example text
symptoms, rec_med, cur_med, diagnosis = extract_health_info(example_conversation)
print("\nSymptoms:", ", ".join(symptoms))
print("\nCurrent medications:", ", ".join(cur_med))
print("\nRecommended medications:", ", ".join(rec_med))
print("\nDiagnosis:", ", ".join(diagnosis))

#Flask app for converting to json
app = Flask(__name__)
# Define a route for the resource
@app.route('/keywords', methods=['GET']) #go to http://127.0.0.1:5000/keywords to see the json output
def get_keywords():
    inputData = str(take_input()) #replace "example_conversation" here with "str(take_input())" to use the voice command input of a conversation
    symptoms, rec_med, cur_med, diagnosis = extract_health_info(inputData)
    return jsonify({
        'symptoms': symptoms,
        'recommended_medications': rec_med,
        'current_medications': cur_med,
        'diagnosis': diagnosis
    })
CORS(app) #cross-origin resource sharing
    
if __name__ == '__main__':
    app.run() 
