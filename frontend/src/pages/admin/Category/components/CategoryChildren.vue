<template>
    <div v-if="category">
        <h6 class="mb-3">
            Danh mục cha:
            <strong>{{ category.name }}</strong>
            ({{ categoryGender(category.gender) }})
        </h6>

        <!-- Nếu không có danh mục con -->
        <div v-if="category.children.length === 0" class="alert alert-warning mb-0">
            Không có danh mục con
        </div>

        <!-- Danh sách danh mục con -->
        <ul v-else class="list-group">
            <li v-for="child in category.children" :key="child.id"
                class="list-group-item d-flex justify-content-between align-items-center">
                <div class="d-flex align-items-center">
                    <img v-if="child.img" :src="child.img.url" class="category-img mr-3" />
                    <div>
                        <strong>{{ child.name }}</strong>
                        <div class="text-muted small">
                            {{ child.gender }}
                        </div>
                    </div>
                </div>

                <span class="badge" :class="child.status ? 'badge-success' : 'badge-secondary'">
                    {{ child.status ? 'Hoạt động' : 'Ẩn' }}
                </span>
            </li>
        </ul>
    </div>
</template>
<script setup lang="ts">
import type { CategoryType } from '@/types/entities';
import { categoryGender } from '@/utils/translateFromEnum';

defineProps<{
    category?: CategoryType
}>()
</script>