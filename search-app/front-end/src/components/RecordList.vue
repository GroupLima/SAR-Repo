<script setup>
import { onMounted } from 'vue';
import Record from '@/components/Record.vue';

const props = defineProps({
    records: {
        type: Object,
        required: true
    }
})
</script>

<template>
    <div class="records">
        <div v-for="record in records" :key="record.id" class="record-item">
            <Record :record="record"/>
        </div>
    </div>
</template>