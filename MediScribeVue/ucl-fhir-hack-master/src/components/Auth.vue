<template>
  <v-container class="fill-height">
    <v-responsive class="align-center text-center fill-height">
      

      <v-row class="d-flex align-center justify-center">
        

        <v-col cols="auto">
          <v-btn
            color="primary"
            min-width="228"
            rel="noopener noreferrer"
            size="x-large"
            target="_blank"
            variant="flat"
            @click="check"
          >
            <v-icon
              icon="mdi-login"
              size="large"
              start
            />

            Authenticate
          </v-btn>
        </v-col>

        
      </v-row>
    </v-responsive>
  </v-container>
</template>

<script setup>
  const check = () => {
    console.log('clicked');
  }
</script>
