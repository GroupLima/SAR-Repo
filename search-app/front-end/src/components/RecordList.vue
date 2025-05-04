<script setup>
import Record from '@/components/Record.vue'
import pageImage from '@/assets/images/try_one.jpeg';
const props = defineProps({
    records: {
        type: Object,
        required: true
    }
})
</script>

<template>
    <div class="records">
        <div v-for="record in props.records" :key="record.id" class="record-item">
            <Record :record="record"/>
        </div>
    </div>
</template>