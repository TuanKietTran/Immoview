export default defineAppConfig({
  ui: {
    colors: {
      primary: 'green',
      neutral: 'slate'
    }
  },
  organization: {
    full_name: 'Immoview AG',
    slug: 'Immoview',
    description: 'Listings, leads, and performance — in a single dashboard built for the Swiss market.',
    address: {
      first_line: 'Bahnhofstrasse 10',
      postal_code: '8001',
      city: 'Zürich',
      country: 'Switzerland'
    }
  },
  techs: ['Vue 3', 'React', 'TypeScript', 'Django', 'AWS Lambda', 'Datadog', 'Sentry'],
  subscriptions: [
    {
      label: 'Starter',
      price: 49,
      billing_period: 'month',
      description: 'Perfect for single-agency operations',
      highlighted: false,
      badge: null,
      cta: 'Start free trial',
      features: [
        '1 agency',
        '50 active listings',
        'Lead scoring',
        'Email notifications',
        'Basic analytics'
      ]
    },
    {
      label: 'Growth',
      price: 149,
      billing_period: 'month',
      description: 'For growing multi-agency groups',
      highlighted: true,
      badge: 'Most popular',
      cta: 'Start free trial',
      features: [
        'Up to 5 agencies',
        'Unlimited listings',
        'Priority lead scoring',
        'Multi-channel notifications',
        'Analytics dashboard',
        'API access'
      ]
    },
    {
      label: 'Enterprise',
      price: null,
      billing_period: null,
      description: 'Custom solutions for large networks',
      highlighted: false,
      badge: null,
      cta: 'Contact us',
      features: [
        'Unlimited agencies',
        'Custom integrations',
        '99.9% uptime SLA',
        'Dedicated support',
        'White-label option',
        'On-premise available'
      ]
    }
  ]
})
