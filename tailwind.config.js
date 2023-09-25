/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./src/templates/**/*.html",
        "./src/static/src/**/*.js",
        "./node_modules/flowbite/**/*.js"
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require("flowbite/plugin")
    ],
}
