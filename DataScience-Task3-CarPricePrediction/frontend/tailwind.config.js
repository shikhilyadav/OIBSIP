/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        racingGreen: {
          DEFAULT: '#073B32',
          deep: '#04241E',
          light: '#0B4E42',
        },
        forestGreen: {
          DEFAULT: '#125B48',
          deep: '#0D4436',
          light: '#1B7A62',
          subtle: '#E8F3EE',
        },
        champagne: {
          DEFAULT: '#E6B85C',
          light: '#F5D897',
          dark: '#C99A3E',
          hover: '#D4A446',
        },
        ivory: {
          DEFAULT: '#F7F5F0',
          light: '#FCFBF8',
          dark: '#EFECE3',
        },
        charcoal: {
          DEFAULT: '#202A28',
          muted: '#77827E',
          light: '#42524E',
        },
        softBorder: '#E4E8E1',
        pureWhite: '#FFFFFF',
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['Outfit', 'Plus Jakarta Sans', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace'],
      },
      boxShadow: {
        soft: '0 2px 12px rgba(7, 59, 50, 0.04), 0 1px 3px rgba(7, 59, 50, 0.02)',
        card: '0 4px 20px rgba(7, 59, 50, 0.06), 0 1px 4px rgba(7, 59, 50, 0.03)',
        floating: '0 12px 36px rgba(7, 59, 50, 0.12), 0 4px 12px rgba(7, 59, 50, 0.06)',
      }
    },
  },
  plugins: [],
}
