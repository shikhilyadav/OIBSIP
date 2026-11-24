/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        botanical: {
          canvas: '#F1F6F2',
          workspace: '#F7FAF7',
          card: '#FFFFFF',
          forest: '#285943',
          deep: '#173D2D',
          sage: '#8BAA91',
          mint: '#DFF4E5',
          paleMint: '#EFF8F0',
          lavender: '#EAE7F5',
          amber: '#F7EBDD',
          textPrimary: '#19362A',
          textSecondary: '#728177',
          border: '#E3EBE3',
          setosa: '#76649D',
          versicolor: '#C18E61',
          virginica: '#2C6A50',
        }
      },
      fontFamily: {
        sans: ['Manrope', 'Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace']
      },
      boxShadow: {
        'soft': '0 4px 20px -2px rgba(23, 61, 45, 0.05)',
        'float': '0 10px 30px -4px rgba(23, 61, 45, 0.08)',
        'hero': '0 15px 35px -5px rgba(40, 89, 67, 0.12)'
      }
    },
  },
  plugins: [],
}
