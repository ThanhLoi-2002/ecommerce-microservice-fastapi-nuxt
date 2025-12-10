<template>
  <div class="d-flex flex-column justify-content-center align-items-center" style="min-height: calc(100vh - 70px)">
    <h3>PAGE NOT FOUND</h3>
    <button class="btn btn-primary" @click="goBack">Back</button>
  </div>
</template>

<script setup>
function goBack() {
  window.history.back()
}
</script>