<script setup>
import { reactive, onMounted, onBeforeUnmount } from 'vue';

const props = defineProps({
    loadingText: {
        type: String,
        required: false,
        default: 'Loading'
    }
});

const loadingState = reactive({
    loadingDots: '.',
    loadingInterval: null
});

const startLoadingAnimation = () => {
  let dotCount = 0;
  const dotArray = ['.', '..', '...'];

  loadingState.loadingInterval = setInterval(() => {
    dotCount = (dotCount + 1) % dotArray.length; // Cycle through the dots
    loadingState.loadingDots = dotArray[dotCount];
  }, 500);  // Change dots every 500ms (adjust as needed)
};

onMounted(() => {
  startLoadingAnimation();
});

onBeforeUnmount(() => {
  // Clean up the interval when the component is destroyed
  if (loadingState.loadingInterval) {
    clearInterval(loadingState.loadingInterval);
  }
});
</script>


<template>
    <div class="loading-text">
        {{ loadingText + loadingState.loadingDots }}
    </div>
</template>