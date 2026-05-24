<script setup lang="ts">
const stats = [
  { label: 'Active listings', value: '1,240', progress: 82 },
  { label: 'Pipeline value', value: 'CHF 3.2M', progress: 67 },
  { label: 'New leads', value: '89', progress: 54 },
]
</script>

<template>
  <div class="flex flex-col gap-3 w-full">
    <div
      v-for="stat in stats"
      :key="stat.label"
      class="rounded-xl border border-(--ui-border) bg-(--ui-bg) px-5 py-4 shadow-sm"
    >
      <div class="flex items-baseline justify-between mb-3">
        <span class="text-2xl font-semibold tracking-tight">{{ stat.value }}</span>
        <span class="text-sm text-(--ui-text-muted)">{{ stat.label }}</span>
      </div>
      <div class="h-1.5 rounded-full bg-(--ui-bg-elevated)">
        <div
          class="h-1.5 rounded-full bg-primary transition-all"
          :style="{ width: `${stat.progress}%` }"
        />
      </div>
    </div>

    <div class="rounded-xl border border-(--ui-border) bg-(--ui-bg) px-5 py-6 text-center shadow-sm">
      <UIcon name="i-lucide-bar-chart-2" class="size-8 mx-auto mb-2 text-(--ui-text-muted)" />
      <p class="text-sm font-medium">Lead funnel</p>
      <p class="text-xs text-(--ui-text-muted) mt-0.5">React island</p>
    </div>
  </div>
</template>
