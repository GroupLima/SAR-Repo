<script setup>
import XQueryStuff from '@/components/XQueryStuff.vue';
import { ref } from 'vue';

const queryParams = ref({}); // Or initialize with appropriate default value
</script>

<template>
    <div>
     <XQueryStuff :queryParams="queryParams">This is XQuery view</XQueryStuff>
    </div>
</template>
