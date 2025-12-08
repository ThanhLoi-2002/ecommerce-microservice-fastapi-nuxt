<template>
  <div class="container py-5">
    <h3 class="mb-4 font-weight-bold">Profile</h3>

    <div class="card p-4">
      <div class="row">
        <div class="col-md-3 text-center">
          <img
            src="https://i.pravatar.cc/150?img=15"
            class="rounded-circle mb-3"
            width="120"
          />
        </div>

        <div class="col-md-9">
          <h5 class="font-weight-bold">{{ profile.name }}</h5>
          <p class="text-muted">{{ profile.email }}</p>

          <hr />

          <button class="btn btn-dark">Edit Profile</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const profile = {
  name: "Đoàn Thành Lợi",
  email: "loi@example.com",
};
</script>
