from speech_rec import take_input
import re
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
        'ibuprofen', 'paracetamol', 'metformin', 'antibiotic', 'physical exam',
    ]
    
    diagnosis_keywords = [
        'respiratory infection', 'pneumonia', 'bronchitis', 'asthma', 'COPD',
        'lung cancer', 'COVID-19', 'coronavirus', 'influenza', 'flu',
        'common cold', 'sinusitis', 'allergic rhinitis', 'hay fever',
        'pulmonary embolism', 'pulmonary fibrosis', 'tuberculosis', 'TB',
        'pulmonary hypertension', 'lung abscess', 'pleurisy', 'pleural effusion',
        'cystic fibrosis', 'pulmonary edema', 'ARDS', 'pulmonary nodules','respiratory infection'
    ] 

    

    
    text = text.lower()
    
    # Add placeholders to the text at the start of each part
    text = text.replace('talking about the symptoms', '<symptoms>')
    text = text.replace('talking about the current medications', '<cur_med>')
    text = text.replace('talking about the diagnosis', '<diagnosis>')
    text = text.replace('talking about the recommended medications', '<rec_med>')

    # Split the text into words
    words = text.split()
    
    # Find the parts of the text that correspond to each category
    symptoms_part = " ".join(words[words.index('<symptoms>')+1:words.index('<cur_med>')])
    cur_med_part = " ".join(words[words.index('<cur_med>')+1:words.index('<diagnosis>')])
    diagnosis_part = " ".join(words[words.index('<diagnosis>')+1:words.index('<rec_med>')])
    rec_med_part = " ".join(words[words.index('<rec_med>')+1:])
    
    # Convert the sentence to lowercase
    symptoms, cur_med, diagnosis, rec_med = [], [], [], []
    # Check if the sentence contains a recommendation phrase and any of the rec_med_keywords
    for word in symptoms_keywords:
        if word in symptoms_part:
            symptoms.append(word)
            
    for word in med_keywords:
        if word in cur_med_part:
            cur_med.append(word)
            
    for word in diagnosis_keywords:
        if word in diagnosis_part:
            diagnosis.append(word)
            
    for word in med_keywords:
        if word in rec_med_part:
            rec_med.append(word)

    # Check if the sentence contains a current medication phrase and any of the cur_med_keywords
    
    
    return list(set(symptoms)), list(set(cur_med)), list(set(diagnosis)), list(set(rec_med))

# Example usage
text = "Hello, Doctor. Before we start, this appointment is being recorded and the audio will be deleted after the session. It’s used to fill out your patient information. Is that okay with you? Yeah, fine by me. So how are you, what seems to be the issue? I have had a cough for the past week. Okay, can you tell me more about your cough? It’s kind of chesty and i feel breathless when it happens. Okay, are you currently taking any medication? Yeah, i am taking some paracetamol. antibiotic Alright, having heard your symptoms it’s possible you have a respiratory infection. We can run some tests, and you should do a physical exam. Alright, thank you for your help."
test_speech = ''' talking about the symptoms I have had a cough for the past week 
It’s kind of chesty and i feel breathless when it happens 
talking about the current medications I am taking some paracetamol
talking about the diagnosis You have a respiratory infection 
talking about the recommended medications You should do a physical exam '''


symptoms, cur_med, diagnosis,rec_med = extract_health_info(test_speech)

print("\nSymptoms:", ", ".join(symptoms))
print("\nCurrent medications:", ", ".join(cur_med))
print("\nDiagnosis:", ", ".join(diagnosis))
print("\nRecommended medications:", ", ".join(rec_med))
