<script setup>

const props = defineProps({
    id: String,
    content: String
})

</script>
<!-- view for one entry of the results -->
<template>
    <div>
        <h4>{{ id }}</h4>

        <div v-html="content"></div> <!-- This will render the HTML content inside the div -->
        <br>
    
    </div>
</template>