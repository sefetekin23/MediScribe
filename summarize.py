import re


def extract_health_info(text: str):
   # Define lists of health-related keywords or phrases
   symptoms_keywords = [
       # Common Symptoms
       'pain', 'fatigue', 'fever', 'headache', 'nausea', 'vomiting',
       'diarrhea', 'dizziness', 'breath', 'breathing', 'cough',
       'sore throat', 'muscle aches', 'swelling', 'bruising',
       'rash', 'itching',
   ]
   rec_med_keywords = [
       # Recommended Medications and Procedures
       'paracetamol', 'ibuprofen', 'aspirin', 'antibiotic', 'antidepressant',
       'antipsychotic', 'antihistamine', 'vaccine', 'immunotherapy', 'chemotherapy',
       'painkiller', 'biopsy', 'MRI', 'ultrasound', 'X-ray', 'chemotherapy',
       'radiation therapy', 'blood test', 'urine test', 'CT scan',
       'endoscopy', 'colonoscopy', 'mammogram', 'vaccination',
       'physical therapy', 'occupational therapy', 'speech therapy', 'exam',
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


   return symptoms, rec_med, cur_med


# Example usage
text = """I have a headache and fever, should I take paracetamol?"""
symptoms, rec_med, cur_med = extract_health_info(text)
print("Symptoms:", symptoms)
print("Recommended Medications:", rec_med)
print("Current Medications:", cur_med)