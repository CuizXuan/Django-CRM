<script>
	export let lines = 3;
	export let height = 'h-4';
	export let width = 'w-full';
	export let avatar = false;
	export let card = false;
</script>

<!-- Card Skeleton -->
{#if card}
	<div class="rounded-lg border bg-card p-4 space-y-3">
		<div class="flex items-center space-x-3">
			{#if avatar}
				<div class="h-10 w-10 rounded-full bg-muted shimmer"></div>
			{/if}
			<div class="flex-1 space-y-2">
				<div class="h-4 w-3/4 bg-muted rounded shimmer"></div>
				<div class="h-3 w-1/2 bg-muted rounded shimmer"></div>
			</div>
		</div>
		<div class="space-y-2">
			{#each Array(lines) as _}
				<div class="{height} {width} bg-muted rounded shimmer"></div>
			{/each}
		</div>
	</div>
{:else if avatar}
	<!-- Avatar Skeleton -->
	<div class="flex items-center space-x-3">
		<div class="h-10 w-10 rounded-full bg-muted shimmer"></div>
		<div class="flex-1 space-y-2">
			<div class="h-4 w-3/4 bg-muted rounded shimmer"></div>
			<div class="h-3 w-1/2 bg-muted rounded shimmer"></div>
		</div>
	</div>
{:else}
	<!-- Line Skeletons -->
	<div class="space-y-2">
		{#each Array(lines) as _, i}
			<div
				class="{height} {i === 0 ? width : 'w-' + (Math.random() > 0.5 ? '3/4' : '5/6')} bg-muted rounded shimmer"
			></div>
		{/each}
	</div>
{/if}

<style>
	:global(.shimmer) {
		background: linear-gradient(
			90deg,
			transparent,
			rgba(255, 255, 255, 0.4),
			transparent
		);
		background-size: 200% 100%;
		animation: shimmer 1.5s infinite;
	}

	:global(.dark .shimmer) {
		background: linear-gradient(
			90deg,
			transparent,
			rgba(255, 255, 255, 0.1),
			transparent
		);
		background-size: 200% 100%;
		animation: shimmer 1.5s infinite;
	}
</style>