/** @type {import('tailwindcss').Config} */
const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	darkMode: "class",
	theme: {
		extend: {
			fontFamily: {
				'sans': ['Space Grotesk', ...defaultTheme.fontFamily.sans],
			},
			colors: {
				transparent: "transparent",
				current: "currentColor",
				primary: {
					blue: "rgb(var(--color-primary-blue) / <alpha-value>)",
					green: "rgb(var(--color-primary-green) / <alpha-value>)",
					yellow: "rgb(var(--color-primary-yellow) / <alpha-value>)",
				},
				text: {
					body: "rgb(var(--color-text-body) / <alpha-value>)",
					bold: "rgb(var(--color-text-bold) / <alpha-value>)",
					heading: "rgb(var(--color-text-heading) / <alpha-value>)",
					muted: "rgb(var(--color-text-muted) / <alpha-value>)",
					code: "rgb(var(--color-text-code) / <alpha-value>)",
					link: "rgb(var(--color-text-link) / <alpha-value>)",
					selection: "rgb(var(--color-text-selection) / <alpha-value>)",
				},
				bg: {
					body: "rgb(var(--color-bg-body) / <alpha-value>)",
					code: "rgb(var(--color-bg-code) / <alpha-value>)",
					selection: "rgb(var(--color-bg-selection) / <alpha-value>)",
				},
				border: {
					code: "rgb(var(--color-border-code) / <alpha-value>)",
				},
			},
		},
	},
    safelist: [{
		// always generate classes for primary colors.
		// (tw only generates colors actually referenced in code, see https://stackoverflow.com/questions/71647859/tailwind-css-certain-custom-colors-are-not-working)
		pattern: /(.)-primary-(.)/,
		variants: ['dark', 'hover', 'dark:hover'],
	}],
	plugins: [
		require('@tailwindcss/typography'),
	],
}