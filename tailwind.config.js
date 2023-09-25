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
                "primary-fg": "#141515",
                "primary-bg": "#1e1f1f",
            }
        },
    },
    plugins: [
        require("flowbite/plugin")
    ],
    darkMode: "class"
}
