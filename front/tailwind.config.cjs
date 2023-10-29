/** @type {import('tailwindcss').Config} */
module.exports = {
	mode: 'jit',
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	darkMode: "class",
	theme: {
		extend: {
			colors: {
				'dark': '#2F3540', 
				'light': '#ECF3FF',
				'sh-dark': '#66748c',
				'sh-light': '#B2B7BF',
				'tx-dark': '#C5C6C7',
				'tx-light': '#3A3938',
				'pr-accent': '#DE7437',
				'pr-muted': '#804320',
				'sc-accent': '#6698D9',
				'sc-muted': '#2A3E59',
				'th-accent': '#ED9C05',
				'th-muted': '#AB7003',
			},
		},
	},
	plugins: [],
}
