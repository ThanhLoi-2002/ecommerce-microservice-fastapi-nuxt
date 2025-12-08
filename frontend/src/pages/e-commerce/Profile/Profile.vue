<template>
  <div class="container py-5">
    <h3 class="mb-4 font-weight-bold">Profile</h3>

    <div class="card p-4">
      <div class="row">

        <!-- Avatar -->
        <div class="col-md-3 text-center">
          <div class="position-relative d-inline-block ">
            <img :src="user?.avatar?.url || DEFAULT_AVATAR" class="rounded-circle border mb-3" width="140" height="140"
              style="object-fit: cover" v-if="!uploadLoading" />

            <!-- Hiển thị hiệu ứng loading -->
            <div v-if="uploadLoading"
              class="rounded-circle border mb-3 d-flex justify-content-center align-items-center"
              style="width: 140px; height: 140px;">
              <img src="@/assets/loading-spinner.svg" alt="Loading..." width="100" height="100" />
            </div>

            <!-- Upload button -->
            <label class="btn btn-sm btn-dark position-absolute" style="bottom: 0; right: 0; border-radius: 50%;">
              <input type="file" class="d-none" accept="image/*" @change="onAvatarChange" :disabled="uploadLoading" />
              <span>📷</span>
            </label>
          </div>
        </div>

        <!-- Info -->
        <div class="col-md-9">

          <!-- View mode -->
          <div v-if="!editing">
            <h5 class="font-weight-bold">{{ user?.name }}</h5>
            <p class="text-muted mb-1">{{ user?.email }}</p>

            <button class="btn btn-dark mt-3" @click="startEdit" :disabled="isLoading">
              Edit Profile
            </button>
          </div>

          <!-- Edit mode -->
          <form v-else @submit.prevent="saveProfile">
            <InputField label="Email" name="email" type="email" v-model="userProfileForm.email!" required
              placeholder="user@gmail.com" />

            <InputField label="Name" name="name" v-model="userProfileForm.name!" required placeholder="Your name"
              :minlength=2 />

            <hr />

            <BaseButton label="Save" :isLoading="isLoading" class="btn btn-dark mr-2" />
            <button class="btn btn-outline-secondary" @click="cancelEdit" type="button">
              Cancel
            </button>
          </form>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import mediaApi from "@/api/media.api";
import { userApi } from "@/api/user.api";
import InputField from "@/components/common/input/InputField.vue";
import { useForm } from "@/composables/useForm";
import { useToast } from "@/composables/useToast";
import { useUpload } from "@/composables/useUpload";
import { useUser } from "@/composables/useUser";
import { useUserStore } from "@/stores/user.store";
import type { AvatarType } from "@/types/entities";
import { DEFAULT_AVATAR } from "@/utils/constants";
import { storeToRefs } from "pinia";
import { ref, watch } from "vue";
import BaseButton from "@/components/common/button/BaseButton.vue";

const { userProfileForm } = useUser()
const { syncForm } = useForm()
const userStore = useUserStore()
const { user, isLoading } = storeToRefs(userStore)
const { upload } = useUpload()
const toast = useToast()

// Edit state
const editing = ref(false);
const uploadLoading = ref(false);

// Khi user thay đổi → cập nhật form
watch(user, (newUser) => {
  syncForm(userProfileForm, newUser)
});

// Bắt đầu edit
const startEdit = () => {
  syncForm(userProfileForm, user.value)
  editing.value = true;
};

// Hủy edit
const cancelEdit = () => {
  editing.value = false;
};

// Upload avatar → preview
const onAvatarChange = async (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (!file) return;

  const result: AvatarType | null = await upload(file)

  if (result) {
    uploadLoading.value = true

    try {
      const { data, message }: any = await userApi.updateAvatar(result)
      await mediaApi.deleteFile(user.value?.avatar?.public_id!)
      userStore.updateUser(data)
      toast.success(message)
    }
    catch (error: any) {
      toast.error(error.message)
    }
    finally {
      uploadLoading.value = false
    }
  }

};

// Lưu profile
const saveProfile = async () => {
  await userStore.updateProfile(userProfileForm, () => {
    editing.value = false;
  })
};
</script>
