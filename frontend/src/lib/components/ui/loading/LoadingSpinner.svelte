<script>
	export let size = 'md';
	export let color = 'primary';
	export let text = '';

	const sizeMap = {
		sm: 'h-4 w-4',
		md: 'h-6 w-6',
		lg: 'h-8 w-8',
		xl: 'h-12 w-12'
	};

	const colorMap = {
		primary: 'text-primary',
		secondary: 'text-secondary',
		muted: 'text-muted-foreground',
		current: 'text-current'
	};
</script>

<div class="flex items-center justify-center gap-3">
	<div
		class="animate-loading {sizeMap[size]} {colorMap[color]}"
		role="status"
		aria-label={text || 'Loading'}
	>
		<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
			<circle
				class="opacity-25"
				cx="12"
				cy="12"
				r="10"
				stroke="currentColor"
				stroke-width="4"
			></circle>
			<path
				class="opacity-75"
				fill="currentColor"
				d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
			></path>
		</svg>
	</div>
	{#if text}
		<p class="text-sm text-muted-foreground animate-pulse">{text}</p>
	{/if}
</div>