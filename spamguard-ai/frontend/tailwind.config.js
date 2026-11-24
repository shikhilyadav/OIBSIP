/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        cyber: {
          bg: '#080D18',
          card: '#0D1422',
          surface: '#111C2E',
          border: '#1E2D44',
          subtle: '#2A3C58',
          accent: '#00F5A0',
          cyan: '#00D9F5',
          danger: '#FF3B5C',
          warning: '#FFB800',
          muted: '#8A99AD'
        }
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace'],
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
