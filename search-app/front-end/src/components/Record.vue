<script setup>

const props = defineProps({
    record: {
        id: {
            type: String,
            required: true
        },
        date: {
            type: String,
            required: false
        },
        language: {
            type: String,
            required: false
        },
        content: {
            type: String,
            required: true
        },
        xml: {
            type: String,
            required: true
        }
    }
    
})
</script>

<template>
    <div>
        <div class="record-header">
        <div>ID: {{ props.record.id }}</div>
        <div>Date: {{ props.record.date }}</div>
        <div>Language: {{ props.record.language }}</div>
    </div>
         <!-- add button to switch between content and xml -->
        <div class="record-content">{{ props.record.content }}</div>
     </div>
</template>