import re

def extract_health_info(text: str):
    # Define lists of health-related keywords or phrases
    symptoms_keywords = [
        'pain', 'fatigue', 'fever', 'headache', 'nausea', 'vomiting',
        'diarrhea', 'dizziness', 'breath', 'breathing', 'breathless', 'cough',
        'sore throat', 'muscle aches', 'swelling', 'bruising',
        'rash', 'itching',
    ]

    cur_med_keywords = [
        'paracetamol', 'ibuprofen', 'aspirin', 'antibiotic', 'antidepressant',
        'antipsychotic', 'antihistamine', 'vaccine', 'immunotherapy', 'chemotherapy',
        'painkiller', 'antibiotic', 'analgesic', 'antidepressant', 'antipsychotic',
        'antihistamine', 'vaccine', 'immunotherapy', 'chemotherapy',
        'radiation', 'surgery', 'transplant', 'dialysis', 'ventilator',
        'anesthesia', 'insulin', 'steroid', 'physical therapy',
        'psychotherapy', 'chiropractic', 'acupuncture', 'homeopathy',
        'hormone therapy', 'antiviral', 'antifungal', 'anticoagulant',
        'statin', 'beta blocker', 'ACE inhibitor', 'aspirin',
        'ibuprofen', 'paracetamol', 'metformin',
    ]

    rec_med_keywords = [
        'ibuprofen', 'aspirin', 'antibiotic', 'antidepressant',
        'antipsychotic', 'antihistamine', 'vaccine', 'immunotherapy', 'chemotherapy',
        'painkiller', 'biopsy', 'MRI', 'ultrasound', 'X-ray', 'chemotherapy',
        'radiation therapy', 'blood test', 'urine test', 'CT scan',
        'endoscopy', 'colonoscopy', 'mammogram', 'vaccination',
        'physical therapy', 'occupational therapy', 'speech therapy', 'physical',
    ]

    # Split the text into words
    text = text.replace("i'm", "im")
    text = text.replace("I'm", "im")
    text = text.replace("I am", "im")
    text = text.replace("i am", "im")
    words = re.findall(r'\b\w+\b', text.lower())  # Extract words while converting to lowercase
   #FIND A WAY TO INCLUDE FULLSTOPS IN WORDS LIST 

    # Extract words that match the keywords for each category
    symptoms = [word for word in words if word in symptoms_keywords]
    rec_med = [word for word in words if word in rec_med_keywords]

    # Extract current medications after each "I'm"
    cur_med = []
    try:
        im_indices = [i for i, word in enumerate(words) if word == "im"]
        for im_index in im_indices:
            taking_index = words.index("taking", im_index) if "taking" in words[im_index:] else -1
            if taking_index == im_index + 1:
                # Find the index of the first period after taking_index
                for word in words[taking_index + 1:]:
                    # Check if the word is in 
                    if "." == word:
                        break
                    elif word in cur_med_keywords:
                        cur_med.append(word)
                    # Check if a period is encountered, and break the loop if true
                    
                
    except ValueError:
        pass

    return list(set(symptoms)), list(set(rec_med)), list(set(cur_med))

# Example usage
text = "Hello, Doctor. Before we start, this appointment is being recorded and the audio will be deleted after the session. It’s used to fill out your patient information. Is that okay with you? Yeah, fine by me. So how are you, what seems to be the issue? I have had a cough for the past week. Okay, can you tell me more about your cough? It’s kind of chesty and i feel breathless when it happens. Okay, are you currently taking any medication? Yeah, i'm taking some paracetamol. antibiotic Alright, having heard your symptoms it’s possible you have a respiratory infection. We can run some tests, and do a physical exam. Alright, thank you for your help."

symptoms, rec_med, cur_med = extract_health_info(text)

print("\nSymptoms:", ", ".join(symptoms))
print("\nCurrent Medications:", ", ".join(cur_med))
print("\nRecommended Medications:", ", ".join(rec_med))
