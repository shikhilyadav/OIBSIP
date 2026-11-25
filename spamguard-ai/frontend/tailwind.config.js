/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        burgundy: {
          DEFAULT: '#542B38',
          deep: '#3D1D27',
          light: '#6E3A4A',
          subtle: '#47222E',
        },
        champagne: {
          DEFAULT: '#D5BDA4',
          light: '#EAE1D7',
          dark: '#BCA085',
        },
        ivory: {
          DEFAULT: '#F5F0E9',
          light: '#FAF7F2',
          surface: '#FFFCF8',
        },
        dustyRose: {
          DEFAULT: '#A56F73',
          light: '#C59599',
          dark: '#855256',
        },
        rosePrimary: {
          DEFAULT: '#A83F55',
          hover: '#8E3346',
          active: '#752838',
          subtle: '#FDF0F2',
        },
        charcoal: {
          DEFAULT: '#33302E',
          muted: '#817A76',
          light: '#595350',
        },
        softBorder: '#E4DAD0',
        whiteSurface: '#FFFCF8',
        status: {
          spam: '#A83F55',
          spamBg: '#FDF0F2',
          spamBorder: '#F5D5DC',
          ham: '#2E6B4F',
          hamBg: '#EFF7F2',
          hamBorder: '#D1E8DA',
          review: '#B87B2E',
          reviewBg: '#FEF8EE',
          reviewBorder: '#F6E6CE',
        }
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace'],
        display: ['Outfit', 'Plus Jakarta Sans', 'sans-serif'],
      },
      boxShadow: {
        soft: '0 2px 10px rgba(84, 43, 56, 0.04), 0 1px 3px rgba(84, 43, 56, 0.02)',
        card: '0 4px 20px rgba(84, 43, 56, 0.06), 0 1px 4px rgba(84, 43, 56, 0.03)',
        floating: '0 12px 36px rgba(84, 43, 56, 0.12), 0 4px 12px rgba(84, 43, 56, 0.06)',
      }
    },
  },
  plugins: [],
}
