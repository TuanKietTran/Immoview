<script setup lang="ts">
const { subscriptions, techs } = useAppConfig()

const agencies = [
  'Helvetia Immobilien', 'ZüriLiving', 'BaselHomes', 'LakeFront Realty',
  'Engel & Zürich', 'AlpineEstate', 'RivaProperties', 'Stadthaus AG'
]

const features = [
  {
    icon: 'i-lucide-layout-dashboard',
    title: 'Listing management',
    description: 'Publish, archive, and bulk-edit listings across all your agencies from a single interface.'
  },
  {
    icon: 'i-lucide-bar-chart-2',
    title: 'Lead scoring',
    description: 'Heuristic scoring engine ranks every inbound lead so your team works the highest-value opportunities first.'
  },
  {
    icon: 'i-lucide-building-2',
    title: 'Agency analytics',
    description: 'Per-agency KPIs — views, conversion rates, pipeline value — updated in real time.'
  },
  {
    icon: 'i-lucide-calculator',
    title: 'Price calculator',
    description: 'CHF/m² valuations with canton-level multipliers and ±15% confidence bands.'
  },
  {
    icon: 'i-lucide-image',
    title: 'Photo pipeline',
    description: 'Automatic image resizing to three CDN-optimised sizes via AWS Lambda and S3.'
  },
  {
    icon: 'i-lucide-bell',
    title: 'Notifications',
    description: 'Email, in-app, and agency webhook notifications driven by SNS — zero polling.'
  }
]

const steps = [
  {
    number: '01',
    title: 'Connect your agencies',
    description: 'Onboard in minutes. Add your agencies, set subscription tiers, and import your first listings via CSV or API.'
  },
  {
    number: '02',
    title: 'Capture and score leads',
    description: 'Every inquiry is queued, scored asynchronously, and surfaced to the right agent — no manual triage needed.'
  },
  {
    number: '03',
    title: 'Act on live analytics',
    description: 'Monitor pipeline health, listing performance, and lead conversion from a single MIS dashboard.'
  }
]
</script>

<template>
  <div>
    <!-- Hero -->
    <UPageHero orientation="horizontal">
      <template #headline>
        <UBadge label="Built for the Swiss market" variant="subtle" color="primary" />
      </template>

      <template #title>
        The operating system for Swiss real estate agencies
      </template>

      <template #description>
        Listings, leads, and performance in a single dashboard. Built for Homegate and ImmoScout24 networks.
      </template>

      <template #links>
        <UButton
          label="Start free trial"
          to="/#pricing"
          size="xl"
          trailing-icon="i-lucide-arrow-right"
        />
        <UButton
          label="View demo"
          to="/docs"
          size="xl"
          color="neutral"
          variant="subtle"
          trailing-icon="i-lucide-play"
        />
      </template>

      <HeroStats />
    </UPageHero>

    <!-- Social proof -->
    <div class="border-y border-(--ui-border) bg-(--ui-bg-muted)/50 py-4">
      <UContainer>
        <div class="flex flex-wrap items-center gap-x-6 gap-y-2">
          <span class="text-sm text-(--ui-text-muted) shrink-0">
            Trusted by 120+ agencies across Zürich, Basel, and Geneva
          </span>
          <div class="flex flex-wrap gap-2">
            <UBadge
              v-for="agency in agencies"
              :key="agency"
              :label="agency"
              color="neutral"
              variant="outline"
              size="md"
            />
          </div>
        </div>
      </UContainer>
    </div>

    <!-- Problem → Solution -->
    <UPageSection
      title="From chaos to clarity"
      description="Most agencies juggle spreadsheets, email threads, and three different portals. Immoview replaces the mess with one system."
    >
      <div class="grid md:grid-cols-2 gap-4 items-center max-w-3xl mx-auto">
        <UPageCard
          title="Before Immoview"
          description="Listings scattered across portals. Leads lost in email. No idea which agency is performing. Manual follow-up for everything."
          icon="i-lucide-x-circle"
          color="error"
          variant="subtle"
        />
        <div class="hidden md:flex justify-center">
          <UIcon name="i-lucide-arrow-right" class="size-8 text-(--ui-text-muted)" />
        </div>
        <UPageCard
          title="After Immoview"
          description="All listings in one place. Leads auto-scored and routed. Real-time analytics per agency. Notifications that just work."
          icon="i-lucide-check-circle"
          color="success"
          variant="subtle"
        />
      </div>
    </UPageSection>

    <!-- Features -->
    <UPageSection
      id="features"
      title="Everything your agency network needs"
      description="Six integrated modules — no duct tape, no missing pieces."
      :features="features"
    />

    <!-- How it works -->
    <UPageSection
      title="Up and running in an afternoon"
      description="No lengthy onboarding, no consultants. Three steps to live."
    >
      <div class="grid md:grid-cols-3 gap-6">
        <div
          v-for="step in steps"
          :key="step.number"
          class="flex flex-col gap-3"
        >
          <span class="text-4xl font-bold text-primary/20 tabular-nums">{{ step.number }}</span>
          <h3 class="text-lg font-semibold">
            {{ step.title }}
          </h3>
          <p class="text-(--ui-text-muted) text-sm leading-relaxed">
            {{ step.description }}
          </p>
        </div>
      </div>
    </UPageSection>

    <!-- Pricing -->
    <UPageSection
      id="pricing"
      title="Simple, transparent pricing"
      description="All plans include a 14-day free trial. No credit card required."
    >
      <div class="grid md:grid-cols-3 gap-6">
        <div
          v-for="plan in subscriptions"
          :key="plan.label"
          class="relative rounded-2xl border p-6 flex flex-col gap-5"
          :class="plan.highlighted
            ? 'border-primary bg-primary/5 shadow-lg'
            : 'border-(--ui-border) bg-(--ui-bg)'"
        >
          <UBadge
            v-if="plan.badge"
            :label="plan.badge"
            color="primary"
            size="sm"
            class="absolute -top-3 left-1/2 -translate-x-1/2"
          />
          <div>
            <p class="text-lg font-semibold">
              {{ plan.label }}
            </p>
            <p class="text-sm text-(--ui-text-muted) mt-0.5">
              {{ plan.description }}
            </p>
          </div>
          <div class="flex items-baseline gap-1">
            <template v-if="plan.price">
              <span class="text-4xl font-bold">CHF {{ plan.price }}</span>
              <span class="text-(--ui-text-muted)">/mo</span>
            </template>
            <span v-else class="text-4xl font-bold">Custom</span>
          </div>
          <ul class="flex flex-col gap-2 flex-1">
            <li
              v-for="feature in plan.features"
              :key="feature"
              class="flex items-center gap-2 text-sm"
            >
              <UIcon name="i-lucide-check" class="size-4 text-primary shrink-0" />
              {{ feature }}
            </li>
          </ul>
          <UButton
            :label="plan.cta"
            :to="plan.price ? '/#' : '/contact'"
            :color="plan.highlighted ? 'primary' : 'neutral'"
            :variant="plan.highlighted ? 'solid' : 'outline'"
            block
            trailing-icon="i-lucide-arrow-right"
          />
        </div>
      </div>
    </UPageSection>

    <!-- Tech credibility -->
    <UPageSection
      title="Built on infrastructure you can trust"
      description="The same stack Swiss Marketplace Group uses — scaled down to agency size."
    >
      <div class="flex flex-wrap justify-center gap-3">
        <UBadge
          v-for="tech in techs"
          :key="tech"
          :label="tech"
          color="neutral"
          variant="subtle"
          size="lg"
        />
      </div>
    </UPageSection>

    <!-- CTA -->
    <UPageSection>
      <UPageCTA
        title="Ready to unify your agency operations?"
        description="Join 120+ Swiss agencies already using Immoview. Start your free 14-day trial today."
        variant="subtle"
        :links="[{
          label: 'Start free trial',
          to: '/#pricing',
          trailingIcon: 'i-lucide-arrow-right'
        }, {
          label: 'Book a demo',
          to: '/contact',
          color: 'neutral',
          variant: 'outline',
          icon: 'i-lucide-calendar'
        }]"
      />
    </UPageSection>
  </div>
</template>
