<script setup>
import { ref, computed, watch, onMounted} from 'vue'

const props = defineProps({
    modelValue: {
        type: String,
        default: '', // Expected format: YYYY-MM-DD
    },
    latestYear: {
        type: Number,
        default: 1512
    },
    earliestYear: {
        type: Number,
        default: 1398
    },
    yearAscending: {
        type: Boolean,
        default: false
    }
})

// allows parent component to see changes in the string date
const emit = defineEmits(['update:modelValue'])

// initalize date parts to null
const selectedYear = ref(null)
const selectedMonth = ref(null)
const selectedDay = ref(null)

// returns a list of years in ascending order
const years = computed(() =>  {
    return Array.from({ length: props.latestYear - props.earliestYear + 1 }, (_, i) => props.earliestYear + i)
})


const months = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]

const days = ref([])

function isLeapYear(year) {
    return (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0
}

// returns number of days depending on month and whether it is a leap year
function getDaysInMonth(year, month) {
    if (month === 2) return isLeapYear(year) ? 29 : 28
    return [4, 6, 9, 11].includes(month) ? 30 : 31
}

// updates the days dropdown list based on leap year and month
function updateDays() {
    if (!selectedYear.value || !selectedMonth.value) {
        days.value = []
        return
    }
    const daysInMonth = getDaysInMonth(selectedYear.value, selectedMonth.value)
    days.value = Array.from({ length: daysInMonth }, (_, i) => i + 1)
    if (selectedDay.value > daysInMonth) {
        selectedDay.value = daysInMonth
    }
}

const tempValues = ref({ year: null, month: null, day: null })

// allows full dropdown to be shown even when the field is nonempty
function forceDropdown(field) {
    // Temporarily clear value to trigger full dropdown
    tempValues.value[field] = { year: selectedYear.value, month: selectedMonth.value, day: selectedDay.value }[field]
    if (field === 'year') selectedYear.value = null
    if (field === 'month') selectedMonth.value = null
    if (field === 'day') selectedDay.value = null
}

const clearInput = () => {
    tempValues.value.year = null
    tempValues.value.month = null
    tempValues.value.day = null
    selectedYear.value = null
    selectedMonth.value = null
    selectedDay.value = null
}

// allow clearInput function to be triggered from parent component
defineExpose({
    clearInput
});

// updates when the user focuses/unfocuses on the field where the selected year/month/day is the current value and temp is the value before focusing on the field
function restoreValue(field) {
    if (field === 'year' && !years.value.includes(selectedYear.value)) {
        selectedYear.value = tempValues.value.year !== null ? tempValues.value.year : null
    }
    if (field === 'month' && !years.value.includes(selectedYear.value)){
        selectedMonth.value = tempValues.value.month !== null ? tempValues.value.month : null
    }
    if (field === 'day' && !years.value.includes(selectedYear.value)){
        selectedDay.value = tempValues.value.day !== null ? tempValues.value.day : null
    }
}

// updates as input changes
watch([selectedYear, selectedMonth, selectedDay], () => {
    const y = selectedYear.value
    const m = selectedMonth.value
    const d = selectedDay.value
    if ( y !== null) {
        let autoMonth = m
        let autoDay = d

        // if for start date, set empty month/day field to first day of the year
        // if for end date, set empty month/day field to last day of the year 

        if (autoMonth === null) {
            autoMonth = props.yearAscending ? 1 : 12
        }
        if (autoDay === null) {
            autoDay = props.yearAscending ? 1 : getDaysInMonth(y, autoMonth)
        }
        // converts data to YYYY-MM-DD format
        const yearString = String(y)
        const monthString = String(autoMonth).padStart(2, '0')
        const dayString = String(autoDay).padStart(2, '0')

        // emit immediate change to parent component
        emit('update:modelValue', `${yearString}-${monthString}-${dayString}`)
  } else {
    emit('update:modelValue', '')
  }
})

onMounted(() => {
    // if date already exists on load, fill out the fields
    if (props.modelValue) {
        const [year, month, day] = props.modelValue.split('-').map(Number)
        selectedYear.value = year
        selectedMonth.value = month
        selectedDay.value = day
    }
    updateDays()
})
</script>

<template>
    <div class="date-picker">
      <!-- Year Input -->
      <input list="years" v-model.number="selectedYear" @focus="forceDropdown('year')" @blur="restoreValue('year')" @change="updateDays" placeholder="Year"
      />
      <datalist id="years">
        <option value="" disabled>Select Year</option> <!-- Empty option for no selection -->
        <option v-for="year in years" :key="year" :value="year"> {{  year }} </option>
      </datalist>
  
      <!-- Month Input -->
      <input list="months" v-model.number="selectedMonth" @focus="forceDropdown('month')" @blur="restoreValue('month')" @change="updateDays" placeholder="Month"
      />
      <datalist id="months">
        <option value="" disabled>Select Month</option> <!-- Empty option for no selection -->
        <option v-for="(month, index) in months" :key="index" :value="index + 1"> {{ month }} </option>
      </datalist>
  
      <!-- Day Input -->
      <input list="days" v-model.number="selectedDay" @focus="forceDropdown('day')" @blur="restoreValue('day')" placeholder="Day"
      />
      <datalist id="days">
        <option value="" disabled>Select Day</option> <!-- Empty option for no selection -->
        <option v-for="day in days" :key="day" :value="day"> {{ day }} </option>
      </datalist>
    </div>
  </template>