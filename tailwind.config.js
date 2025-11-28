// /** @type {import('tailwindcss').Config} */
// module.exports = {
//   content: [
//     "./templates/**/*.html",
//     "./**/templates/**/*.html"
//   ],
//   theme: {
//     extend: {},
//   },
//   plugins: [],
// }

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.{html,js}",
    "./**/templates/**/*.{html,js}",
    "./events/**/*.{html,py}",
    "./**/*.py"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
