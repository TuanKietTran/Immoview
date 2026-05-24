<script setup lang="ts">
import type { FooterColumn } from '@nuxt/ui'

const columns: FooterColumn[] = [
  {
    label: 'Product',
    children: [
      { label: 'Docs', to: '/docs', target: '_self' },
      { label: 'API reference', to: '/docs/api', target: '_self' },
      { label: 'Status', to: 'https://status.immoview.ch', target: '_blank' },
      { label: 'Changelog', to: '/changelog', target: '_self' }
    ]
  },
  {
    label: 'Company',
    children: [
      { label: 'About', to: '/about', target: '_self' },
      { label: 'Contact', to: '/contact', target: '_self' },
      { label: 'Privacy', to: '/legal/privacy', target: '_self' },
      { label: 'Terms', to: '/legal/terms', target: '_self' }
    ]
  }
]

const settings = useAppConfig()
</script>

<template>
  <UFooter>
    <template #left>
      <div class="flex flex-col gap-1.5">
        <div>
          <h1 class="text-3xl">
            {{ settings.organization.slug }}
          </h1>
        </div>
        <p class="text-muted text-sm">
          {{ settings.organization.address.first_line }} <br>
          {{ settings.organization.address.postal_code }}
          {{ settings.organization.address.city }},
          {{ settings.organization.address.country }}
        </p>
        <p class="text-muted text-sm">
          Copyright © {{ new Date().getFullYear() }}
          {{ settings.organization.full_name }}
        </p>
      </div>
    </template>

    <template #right>
      <UContainer>
        <UFooterColumns :columns="columns" />
      </UContainer>
    </template>
  </UFooter>
</template>
