<template>
    <div>
        <v-container grid-list-md text-xs-center>
            <v-layout row wrap>
                <v-flex xs6>
                    <v-card dark color="secondary">
                        <v-img
          src="https://cdn.vuetifyjs.com/images/cards/desert.jpg"
          aspect-ratio="2.75"
                        ></v-img>

                        <v-card-text class="px-0">6</v-card-text>
                    </v-card>
                </v-flex>
                <v-flex xs6>
                    <v-card dark color="secondary">
                        <v-img
                        src="https://cdn.vuetifyjs.com/images/cards/desert.jpg"
                        aspect-ratio="2.75"
                        ></v-img>

                        <v-card-text class="px-0">7</v-card-text>
                    </v-card>
                </v-flex>
            </v-layout>
        </v-container>
    </div>
</template>


<script>
export default {
    name: "Main"
}
</script>
