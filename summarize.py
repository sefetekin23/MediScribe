import re


def extract_health_info(text: str):
   # Define lists of health-related keywords or phrases
   symptoms_keywords = [
       # Common Symptoms
       'pain', 'fatigue', 'fever', 'headache', 'nausea', 'vomiting',
       'diarrhea', 'dizziness', 'breath', 'breathing', 'breathless', 'cough',
       'sore throat', 'muscle aches', 'swelling', 'bruising',
       'rash', 'itching',
   ]
   rec_med_keywords = [
       # Recommended Medications and Procedures
        'ibuprofen', 'aspirin', 'antibiotic', 'antidepressant',
       'antipsychotic', 'antihistamine', 'vaccine', 'immunotherapy', 'chemotherapy',
       'painkiller', 'biopsy', 'MRI', 'ultrasound', 'X-ray', 'chemotherapy',
       'radiation therapy', 'blood test', 'urine test', 'CT scan',
       'endoscopy', 'colonoscopy', 'mammogram', 'vaccination',
       'physical therapy', 'occupational therapy', 'speech therapy', 'physical',
   ]
   cur_med_keywords = [
       # Current Medications
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




   # Split the text into words
   words = re.findall(r'\b\w+\b', text.lower())  # Extract words while converting to lowercase




   # Extract words that match the keywords for each category
   symptoms = [word for word in words if word in symptoms_keywords]
   rec_med = [word for word in words if word in rec_med_keywords]
   cur_med = [word for word in words if word in cur_med_keywords]


   return list(set(symptoms)), list(set(rec_med)), list(set(cur_med))


# Example usage
text = "Hello, Doctor. Before we start, this appointment is being recorded and the audio will be deleted after the session. It’s used to fill out your patient information. Is that okay with you? Yeah, fine by me. So how are you, what seems to be the issue? I have had a cough for the past week. Okay, can you tell me more about your cough? It’s kind of chesty and i feel breathless when it happens. Okay, are you currently taking any medication? Yeah, im taking some paracetamol. Alright, having heard your symptoms it’s possible you have a respiratory infection. We can run some tests, and do a physical exam. Alright, thank you for your help."
symptoms, rec_med, cur_med = extract_health_info(text)


print("\nSymptoms:", ", ".join(symptoms))
print("\nCurrent Medications:", ", ".join(cur_med))
print("\nRecommended Medications:", ", ".join(rec_med))
