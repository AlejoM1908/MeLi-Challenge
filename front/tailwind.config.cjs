/** @type {import('tailwindcss').Config} */
module.exports = {
	mode: 'jit',
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	darkMode: "class",
	theme: {
		extend: {
			colors: {
				'dark': '#262626', 
				'light': '#FFFFFF',
				'sh-dark': '#303030',
				'sh-light': '#EBEBEB',
				'tx-dark': '#FFFFFF',
				'border-dark': '#ACB2BB',
				'border-light': '#DDDDDD',
				'tx-light': '#000000',
				'pr-accent': '#FFF159',
				'pr-muted': '#FFF159',
				'sc-accent': '#232D7C',
				'sc-muted': '#232D7C',
				'th-accent': '#A90F90',
				'th-muted': '#0F1A53',
				'bu-color': '#3483FA',
				'bu-hover': '#2968c8'
			},
		},
	},
	plugins: [],
}
