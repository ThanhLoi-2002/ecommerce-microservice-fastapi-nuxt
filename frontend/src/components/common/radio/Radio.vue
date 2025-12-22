<template>
    <div class="form-group">
        <label>{{ label }}</label>
        <div class="d-flex" style="cursor: pointer;">
            <div v-for="(option, index) in options" :key="index" class="form-check mx-1 d-flex align-items-center">
                <input type="radio" :id="option.value" :value="option.value" class="form-check-input"
                    style="cursor: pointer;" v-model="selectedOption" :name="name" @change="updateSelectedOption" />
                <label class="form-check-label" :for="option.value" style="cursor: pointer;">{{ option.label }}</label>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { OptionType } from '@/types/common';
import { ref } from 'vue';

const props = defineProps<{
    options: OptionType[],
    label: string
    value: string
    name: string
    chooseRadio: (value: any) => void
}>();

const selectedOption = ref(props.value); // Default to the first option

// Update the selected option and notify the parent when it changes
const updateSelectedOption = (e: any) => {
    props.chooseRadio(e.target.value); // Notify the parent about the selected value
    selectedOption.value = e.target.value
};
</script>