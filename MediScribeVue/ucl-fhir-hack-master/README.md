# Testing the GOSH FHIR API

Kindly be aware that the API in use is an Azure FHIR API, and for the purposes of the Hack, [synthetic FHIR data](https://mitre.box.com/shared/static/ydmcj2kpwzoyt6zndx4yfz163hfvyhd0.zip) has been loaded into it using [FhirLoader](https://github.com/hansenms/FhirLoader) as recommended by Microsoft Azure for FHIR API developers.

This simple `smart-on-fhir application` essentially calculates the occurrence count of specified `Conditions` within a chosen `year`.

## Project setup and compilation

Download the repository. 

``` git clone https://github.com/gosh-dre/ucl-fhir-hack.git ```

Make sure you have `npm`, `Vue.js`, and Node.js v4 installed. If you don't have them yet installed, we recommend using [`nvm`](https://github.com/creationix/nvm) and [`Vue.js`](https://vuejs.org/).

Once you're in the root directory, create a file named `.env` and insert your `token` in the format ``` VITE_TOKEN="add-token-here" ```. 

Afterward, execute the application by running either of the following:

```
# yarn
yarn

# npm
npm install

```

### Compiles and hot-reloads for development

```
# yarn
yarn dev

# npm
npm run dev

To compile and hot-reload on a specified port (example 8006), run

```bash
npm run dev -- --port 8006
``` 

##
**Please Note** The `token` will be issued to you before the Hackathon.
