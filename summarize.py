import re
from speech_rec import take_input

def extract_health_info(text: str):
    symptoms_keywords = [
        'pain', 'fatigue', 'fever', 'headache', 'nausea', 'vomiting',
        'diarrhea', 'dizziness', 'breathing', 'breathless', 'cough',
        'sore throat', 'muscle aches', 'swelling', 'bruising',
        'rash', 'itching',
    ]

    med_keywords = [
        'paracetamol', 'ibuprofen', 'aspirin', 'antibiotic', 'antidepressant',
        'antipsychotic', 'antihistamine', 'vaccine', 'immunotherapy', 'chemotherapy',
        'painkiller', 'antibiotic', 'analgesic', 'antidepressant', 'antipsychotic',
        'antihistamine', 'vaccine', 'immunotherapy', 'chemotherapy',
        'radiation', 'surgery', 'transplant', 'dialysis', 'ventilator',
        'anesthesia', 'insulin', 'steroid', 'physical therapy',
        'psychotherapy', 'chiropractic', 'acupuncture', 'homeopathy',
        'hormone therapy', 'antiviral', 'antifungal', 'anticoagulant',
        'statin', 'beta blocker', 'ACE inhibitor', 'aspirin',
        'ibuprofen', 'paracetamol', 'metformin', 'antibiotic', 'physical'
    ]
    
    diagnosis_keywords = [
        'respiratory infection', 'pneumonia', 'bronchitis', 'asthma', 'COPD',
        'lung cancer', 'COVID-19', 'coronavirus', 'influenza', 'flu',
        'common cold', 'sinusitis', 'allergic rhinitis', 'hay fever',
        'pulmonary embolism', 'pulmonary fibrosis', 'tuberculosis', 'TB',
        'pulmonary hypertension', 'lung abscess', 'pleurisy', 'pleural effusion',
        'cystic fibrosis', 'pulmonary edema', 'ARDS', 'pulmonary nodules',
    ] 
    
    # Define phrases that typically indicate a recommendation or a statement of current medication
    rec_phrases = ["i recommend", "you should", "try taking"]
    cur_phrases = ["i am taking", "i have been prescribed", "my current medication is"]

    # Split the text into sentences
    sentences = re.split(r'[.!?]', text)

     # Initialize the lists for recommended and current medications
    rec_med = []
    cur_med = []

    # Convert the text to lowercase
    text = text.lower()

    # Split the text into words
    words = text.split()

    # Iterate over the words
    for i, word in enumerate(words):
        # If the word is a med keyword, check if the previous word was a rec phrase or a cur phrase
        if word in med_keywords:
            # Get the part of the text before the current word
            prev_text = ' '.join(words[max(0, i-5):i]) #gets last 5 words before the current word

            # If a rec phrase is in the previous text, add the current word to rec_med
            if any(phrase in prev_text for phrase in rec_phrases):
                rec_med.append(word)
            # If a cur phrase is in the previous text, add the current word to cur_med
            elif any(phrase in prev_text for phrase in cur_phrases):
                cur_med.append(word)

    # Extract words that match the keywords for each category
    symptoms = [word for word in symptoms_keywords if word in text]
    diagnosis = [word for word in diagnosis_keywords if word in text]

    return list(set(symptoms)), list(set(rec_med)), list(set(cur_med)), list(set(diagnosis))

# Example usage
text = "Hello, Doctor. Before we start, this appointment is being recorded and the audio will be deleted after the session. It’s used to fill out your patient information. Is that okay with you? Yeah, fine by me. So how are you, what seems to be the issue? I have had a cough for the past week. Okay, can you tell me more about your cough? It’s kind of chesty and i feel breathless when it happens. Okay, are you currently taking any medication? Yeah, i am taking some paracetamol. antibiotic Alright, having heard your symptoms it’s possible you have a respiratory infection. We can run some tests, and you should do a physical exam. Alright, thank you for your help."
test_speech = ''' I have had a cough for the past week 
it’s kind of chesty and i feel breathless when it happens 
I am taking some paracetamol
you have a respiratory infection 
you should do a physical exam '''

b = str(take_input())
print(b)
symptoms, rec_med, cur_med, diagnosis = extract_health_info(b)

print("\nSymptoms:", ", ".join(symptoms))
print("\nCurrent medications:", ", ".join(cur_med))
print("\nRecommended medications:", ", ".join(rec_med))
print("\nDiagnosis:", ", ".join(diagnosis))
