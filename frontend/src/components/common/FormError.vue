// <script setup>
// const props = defineProps(["errors"]);
// </script>
// <template>
//   <div :class="{ error: props.errors.length }">
//     <slot></slot>

//     <div class="input-errors" v-for="error of props.errors" :key="error.$uid">
//       <div class="error-msg" style="color: red; font-weight: bold">
//         {{ error.$message }}
//       </div>
//     </div>
//   </div>
// </template>
<template>
  <div v-if="errors && errors.length" class="mt-1">
    <p
      v-for="(err, index) in errors"
      :key="index"
      class="text-red-500 text-xs"
    >
      {{ err }}
    </p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  errors?: string[] | undefined
}>()
</script>
