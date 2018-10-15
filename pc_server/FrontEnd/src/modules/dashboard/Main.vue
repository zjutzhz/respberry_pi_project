<template>
    <div>
        <v-container grid-list-md text-xs-center>
            <v-layout row wrap>
                <v-flex xs6>
                    <image-card  v-bind:image_url= "capture_image"></image-card>
                </v-flex>
                <v-flex xs6>
                    <v-card dark color="secondary">
                        <v-img
                        src="https://cdn.vuetifyjs.com/images/cards/desert.jpg"
                        aspect-ratio="2.75"
                        ></v-img>

                        <v-card-text class="px-0">8</v-card-text>
                    </v-card>
                </v-flex>
            </v-layout>
        </v-container>
    </div>
</template>


<script>
import ImageCard from "@/modules/dashboard/components/ImageCard"
export default {
    name: "Main",
    data: function() {
        return {
            capture_image: "",
            timer: ""
        }
    },
    created : function () {
        this.capture_image = "https://cdn.vuetifyjs.com/images/cards/docks.jpg"
        this.timer = setInterval(this.updateCaptureUrl, 1000)
    },
    methods: {
        updateCaptureUrl : function(){
            fetch( "/api/v1/recent_capture_image_name", {methods:"GET"})
            .then(resp => resp.text())
            .then(path => {
                if (this.capture_image != path) {
                    this.capture_image = path
                }
            })
        } ,
        cancelAutoUpdate: function() { clearInterval(this.timer) }
    },
    beforeDestroy: function() {
       clearInterval(this.timer)
    },
    components: {
        "image-card": ImageCard
    }
    
}
</script>
