<script setup>
useHead({
  meta: [
    { name: 'viewport', content: 'width=device-width, initial-scale=1' }
  ],
  link: [
    { rel: 'icon', href: '/favicon.ico' }
  ],
  htmlAttrs: {
    lang: 'en'
  }
})

const { organization } = useAppConfig()

useSeoMeta({
  title: 'Immoview',
  description: organization.description,
  ogTitle: organization.full_name,
  ogDescription: organization.description,
  twitterCard: 'summary_large_image'
})

const navLinks = [
  { label: 'Product', to: '/#features' },
  { label: 'Pricing', to: '/#pricing' },
  { label: 'Docs', to: '/docs' }
]
</script>

<template>
  <UApp>
    <UHeader>
      <template #left>
        <NuxtLink to="/">
          <AppLogo class="w-auto h-6 shrink-0" />
        </NuxtLink>
        <nav class="hidden md:flex items-center gap-0.5 ml-4">
          <UButton
            v-for="link in navLinks"
            :key="link.label"
            :label="link.label"
            :to="link.to"
            color="neutral"
            variant="ghost"
            size="sm"
          />
        </nav>
      </template>

      <template #right>
        <UButton
          label="Sign in"
          to="/login"
          color="neutral"
          variant="ghost"
          size="sm"
        />
        <UButton
          label="Start free trial"
          to="/#pricing"
          size="sm"
          trailing-icon="i-lucide-arrow-right"
        />
      </template>
    </UHeader>

    <UMain>
      <NuxtPage />
    </UMain>

    <USeparator />

    <AppFooter />
  </UApp>
</template>
