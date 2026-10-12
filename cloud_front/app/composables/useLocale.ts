import en from '../../i18n/locales/en'
import vi from '../../i18n/locales/vi'

export type Locale = 'en' | 'vi'
const messages = { en, vi }

export function useLocale() {
  const locale = useState<Locale>('locale', () => 'vi')
  const t = (key: keyof typeof en) => messages[locale.value][key]
  return { locale, t, messages }
}
