<template>
    <div>
        <v-card dark color="secondary">
                            <v-img
            v-bind:src="image_url"
            aspect-ratio="2.75"
            ></v-img>
            <v-card-text class="px-0">6</v-card-text>
        </v-card>
    </div>
</template>

<script>
export default {
    name: "ImageCard",
    props: ["image_url"]
}
</script>

