/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./src/templates/**/*.html",
        "./src/static/src/**/*.js",
        "./node_modules/flowbite/**/*.js"
    ],
    theme: {
        extend: {
            colors: {
                "primary-fg": "#091012",
                "primary-bg": "#181a1b",
            }
        },
    },
    plugins: [
        require("flowbite/plugin")
    ],
    darkMode: "class"
}
