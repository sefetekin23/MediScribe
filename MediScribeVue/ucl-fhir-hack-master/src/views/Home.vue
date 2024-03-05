<template>
  <v-container class="fill-height">
    <v-responsive class=" fill-height">
      <v-row class="d-flex justify-center mt-10">
        <v-col cols="auto">
          <v-btn  @click="submit" :loading="isLoading" ripple color="#5865f2" class="d-inline"
            size="x-large">
            Submit
          </v-btn>
        </v-col> 
      </v-row>
      <v-snackbar color="red" v-model="snackbar" timeout="2000">
        Internal error... please try again later
      </v-snackbar>

      <v-row class="d-flex justify-center mt-10">
        <v-col>
          <v-text-field label="Patient Full Name" v-model="name"></v-text-field>
          <v-text-field label="Phone no." v-model="phone"></v-text-field>
          <v-text-field label="Email address" v-model="email"></v-text-field>
          <v-text-field label="Date of Birth" v-model="dob"></v-text-field>
        </v-col>

        <v-col>
          <v-text-field label="Name of GP" v-model="gp"></v-text-field>
          <v-text-field label="Date of Appointment" v-model="date"></v-text-field>
          <!-- <v-text-field label="Time of Appointment" v-model="time"></v-text-field> -->
        </v-col>
      </v-row>




      <v-row>
        <v-col>
          <v-divider></v-divider>
        </v-col>
      </v-row>



      <v-row class="d-flex justify-center mt-10">
        <v-col>
          <v-text-field label="Symptoms" v-model="symptoms"></v-text-field>
          <v-text-field label="Diagnosis" v-model="diagnosis"></v-text-field>
        </v-col>
        <v-col>
          <v-text-field label="Current Medication" v-model="currentMedication"></v-text-field>
          <v-text-field label="Prescribed Medication" v-model="prescribedMedication"></v-text-field>
        </v-col>
      </v-row>


      <v-data-table :headers="headers" :items="appointments" class="elevation-1">
      </v-data-table>
<!-- 
      <v-btn @click="updateAppointments" :loading="isLoading" ripple color="#5865f2" class="d-inline" size="x-large">
        Update Appointment
      </v-btn> -->


      <v-btn @click="initialise" :loading="isLoading" ripple color="#5865f2" class="d-inline" size="x-large">
        Initialise Healthcare Database
      </v-btn>


      <v-btn @click="listening" :loading="isLoading" ripple color="#5865f2" class="d-inline" size="x-large">
        Start Listening
      </v-btn>



    </v-responsive>
  </v-container>
</template>

<script setup>
import { ref, computed, toRefs } from 'vue'
import axios from 'axios'


let name = ref('');
let phone = ref('');
let date = ref('');
let email = ref('');
let dob = ref('');
let gp = ref('');

// Listen button for auto-fill
let symptoms = ref('');
let currentMedication = ref('');
let prescribedMedication = ref('');
let diagnosis = ref('');

const isLoading = ref(false)
const outcome = ref('--')

const baseURL = 'http://localhost:8080/fhir';




let appointments = ref([]);
const headers = [
  { title: 'Appointment ID', value: 'id' },
  { title: 'Patient', value: 'patientName' },
  { title: 'Practitioner', value: 'practitionerName' },
  { title: 'Symptoms', value: 'symptoms' },
  { title: 'Current Medication', value: 'currentMedication' },
  { title: 'Prescribed Medication', value: 'prescribedMedication' },
  { title: 'Diagnosis', value: 'diagnosis' },
];
// Update appointments table
const updateAppointments = async () => {
  try {

    appointments.value = [];
    const response = await axios.get(`${baseURL}/Appointment`);

    console.log(response);

    for (let element of response.data.entry) {
      let appointmentDate = element.resource.end;

      
      const patientResponse = await axios.get(`${baseURL}/Patient/${(element.resource.participant[1].actor.reference).slice(-1)}`);
      let patientString = patientResponse.data.name[0].text;
      let patientPhone = patientResponse.data.telecom[0].value;
      let patientEmail = patientResponse.data.telecom[1].value;
      let patientBirthDate = patientResponse.data.birthDate;


      const practitionerResponse = await axios.get(`${baseURL}/Practitioner/${(element.resource.participant[0].actor.reference).slice(-1)}`);
      let practitionerString = practitionerResponse.data.name[0].text;

      const encounterResponse = await axios.get(`${baseURL}/Encounter/?appointment=${element.resource.id}`);
      let encounterId = encounterResponse.data.entry[0].resource.id;

      const observationResponse = await axios.get(`${baseURL}/Observation/?encounter=${encounterId}`);
      let observationString = observationResponse.data.entry[0].resource.valueString;

      // Doesnt allow search term from encounters, this is a weakness of the fhir sandbox server being used
      // const medicationStatementResponse = await axios.get(`${baseURL}/MedicationStatement/?encounter=${element.resource.id}`);
      // console.log(medicationStatementResponse.data.id);
      let currentMedication = element.resource.comment;

      const carePlanResponse = await axios.get(`${baseURL}/CarePlan/?encounter=${encounterId}`);
      let carePlanString = carePlanResponse.data.entry[0].resource.activity[0].detail.code.text;

      const conditionResponse = await axios.get(`${baseURL}/Condition/?encounter=${encounterId}`);
      let conditionString = conditionResponse.data.entry[0].resource.code.text

      appointments.value.push({
        patientName: patientString,
        practitionerName: practitionerString,
        id: element.resource.id,
        symptoms: observationString,
        currentMedication: currentMedication, // Update this as needed
        prescribedMedication: carePlanString,
        diagnosis: conditionString,
      });
    }


  } catch (error) {
    console.log(error);

  }
};
updateAppointments();



const listening = async () => {
  const response = await axios.get('http://127.0.0.1:5000/keywords');


  currentMedication.value = response.data.current_medications.join(', ');
  diagnosis.value = response.data.diagnosis.join(', ');
  prescribedMedication.value = response.data.recommended_medications.join(', ');
  symptoms.value = response.data.symptoms.join(', ');


}

// Submit for new appointment
const submit = async () => {
  isLoading.value = true;
  outcome.value = '--';

  try {

    await createAppointment();
    
    isLoading.value = false;
    outcome.value = 'Appointment created successfully';
  } catch (error) {
    console.log(error);
    isLoading.value = false;
    // snackbar.value = true;
    outcome.value = '--';
  }


};

let patientId;
let practitionerId;
let appointmentId;
let encounterId;
let observationId;
let medicationStatementId;
let carePlanId;
let diagnosisId;

const createAppointment = async () => {
  isLoading.value = true;
  outcome.value = '--';

  patientId = await findPerson(name.value, "Patient");
  practitionerId = await findPerson(gp.value, "Practitioner");
  console.log("Patient ID:", patientId);
  console.log("Practitioner ID:", practitionerId);
  try {

    const appointmentPayload = {
      "resourceType": "Appointment",
      "status": "fulfilled",
      "participant": [{
        "actor": {
          "reference": `Practitioner/${practitionerId}`
        }
      }, {
        "actor": {
          "reference": `Patient/${patientId}`
        }
      }],
      "reason": "",
      "comment": `${currentMedication.value}`,
      "start": `${date.value}`,
      "end": `${date.value}`,
      "supportingInformation": "None"
    };
    const response = await apiPost('Appointment', appointmentPayload, 'Appointment');
    appointmentId = response.data.id;

    // Symptoms, Currnet Meidcation, Prescribed Medication, Diagnosis
    encounterId = await createEncounter(appointmentId); // Used to link all successive entries
    observationId = await createObservation(encounterId, symptoms.value); // Stores Symptoms
    // Medication Statment (currnet medication) is captured in comment of appointmnet
    // medicationStatementId = await createMedicationStatement(encounterId, currentMedication.value); 
    carePlanId = await createCarePlan(encounterId, prescribedMedication.value); // Stores Prescribed Medication
    diagnosisId = await createCondition(encounterId, diagnosis.value); // Stores diagnosis
    await updateAppointments();
  }
  catch (error) {
    console.log(error);
  }

};


const findPerson = async (name, typePerson) => {
  isLoading.value = true;
  outcome.value = '--';

  try {
    const response = await axios.get(`${baseURL}/${typePerson}?name=${name}&_pretty=true`, {
      headers: {
        'Content-Type': 'application/fhir+json'
      }
    });

    console.log(`Successfully found ${typePerson}:`, response.data);
    return response.data.entry[0].resource.id;
  } catch (error) {
    console.log(error);
    console.log(typePerson)
    console.log(`Error finding person ${typePerson}:`, error);
    throw error;
  }
};

const createEncounter = async (appointmentId) => {
  try {
    const encounterPayload = {
      "resourceType": "Encounter",
      "status": "finished",
      "appointment": {
        "reference": `Appointment/${appointmentId}`
      }
    };
    const response = await apiPost('Encounter', encounterPayload, 'Encounter');
    return response.data.id;
  }
  catch (error) {
    console.log(error)
  }
};

const createObservation = async (encounterId, symptoms) => {
  try {
    const observationPayload = {
      "resourceType": "Observation",
      "status": "final",
      "encounter": {
        "reference": `Encounter/${encounterId}`
      },
      "valueString": `${symptoms}`

    };
    const response = await apiPost('Observation', observationPayload, 'Observation');
    return response.data.id;
  }
  catch (error) {
    console.log(error)
  }

};

const createMedicationStatement = async (encounterId, currentMedication) => {
  try {
    const medicationStatementPayload = {
      "resourceType": "MedicationStatement",
      "clinicalStatus": "active",
      "verificationStatus": "confirmed",
      "medicationCodeableConcept": {
        "text": `${currentMedication}`
      },
      "derivedFrom": {
        "reference": `Encounter/${encounterId}`
      }
    };
    const response = await apiPost('MedicationStatement', medicationStatementPayload, 'MedicationStatement');
    return response.data.id;
  }
  catch (error) {
    console.log(error)
  }

};

const createCarePlan = async (encounterId, prescribedMedication) => {
  try {
    const carePlanPayload = {
      "resourceType": "CarePlan",
      "status": "active",
      "intent": "proposal",
      "activity": [
        {
          "detail": {
            "status": "in-progress",
            "code": {
              "text": `${prescribedMedication}`
            }
          }
        }
      ],
      "encounter": {
        "reference": `Encounter/${encounterId}`
      }
    };
    const response = await apiPost('CarePlan', carePlanPayload, 'CarePlan');
    return response.data.id;
  }
  catch (error) {
    console.log(error)
  }

}

const createCondition = async (encounterId, diagnosis) => {
  try {
    const conditionPayload = {
      "resourceType": "Condition",
      "clinicalStatus": {
        "text": "Active"
      },
      "verificationStatus": {
        "text": "Confirmed"
      },
      "code": {
        "text": `${diagnosis}`
      },
      "encounter": {
        "reference": `Encounter/${encounterId}`
      }
    };
    const response = await apiPost('Condition', conditionPayload, 'Condition');
    return response.data.id;
  }
  catch (error) {
    console.log(error)
  }

};

// Initialise Database with some fake customers and practitioners
let organizationId;
let patientName = "Ben Cook";
let practitionerName = "Mohamad El Habbal";
let dateAppointment = "2005-12-12";


const initialise = async () => {
  isLoading.value = true;
  outcome.value = '--';

  try {
    await createOrganization();
    await createPractitioner();
    await createPatient();

    isLoading.value = false;
    outcome.value = 'Initialization completed successfully';
  } catch (error) {
    isLoading.value = false;
    snackbar.value = true;
    outcome.value = '--';
  }
};

const createOrganization = async () => {
  try {
    const organizationPayload = {
      "resourceType": "Organization",
      "name": "Giggie Grove Healthcentre"
    };

    const response = await apiPost('Organization', organizationPayload, 'Organization');
    organizationId = response.data.id;
  } catch (error) {

  }
};

const createPatient = async () => {
  try {
    const patientPayload = {
      "resourceType": "Patient",
      "name": [{
        "text": "Ben Cook"
      }],
      "birthDate": "2000-10-31",
      "telecom": [{
        "system": "phone",
        "value": "07491823847"
      }, {
        "system": "email",
        "value": "thenewjoeshmoe@joeshmoe.com"
      }],
      "managingOrganization": {
        "reference": `Organization/${organizationId}`  // Use the organizationId here
      }
    };

    const response = await apiPost('Patient', patientPayload, 'Patient');
    //patientId = response.data.id;  // Extract the ID from the response
  } catch (error) {
    console.error(error);
    throw error;
  }
};

const createPractitioner = async () => {
  try {
    const practitionerPayload = {
      "resourceType": "Practitioner",
      "name": [{
        "text": "Mohamad El Habbal"
      }],
      "birthDate": "1954-03-10",
      "telecom": [{
        "system": "phone",
        "value": "1028884029"
      }, {
        "system": "email",
        "value": "drmohamad@mohamad.com"
      }],
      "managingOrganization": {
        "reference": `Organization/${organizationId}`  // Use the organizationId here
      }
    };

    const response = await apiPost('Practitioner', practitionerPayload, 'Practitioner');
    //practitionerId = response.data.id;  // Extract the ID from the response
  } catch (error) {
    // Handle error if needed
  }
};


const apiPost = async (url, payload, resourceType) => {
  try {
    const response = await axios.post(`${baseURL}/${url}?_format=json&_pretty=true`, payload, {
      headers: {
        'Content-Type': 'application/fhir+json'
      }
    });

    console.log(`Successfully created ${resourceType}:`, response.data);
    return response;
  } catch (error) {
    console.log(error);
    console.error(`Error creating ${resourceType}:`, error);
    throw error;
  }
};


</script>


<style lang="scss">
.output {

  h3 {
    text-align: center;
    letter-spacing: 0.167rem;
  }

  div {
    padding: 0.25em 1.5em;
    aspect-ratio: 1;
    background-color: #f6f6f6;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 2.5rem;
    font-weight: bold;
    color: #5865f2;
    border: 1px dashed #ddd;
  }


}
</style>