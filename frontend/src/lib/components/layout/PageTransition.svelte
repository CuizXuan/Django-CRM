<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';

	/** @type {import('svelte').Snippet} [children] - Child content */
	let { children, class: className = '' } = $props();

	let isVisible = $state(false);

	onMount(() => {
		// 触发页面过渡动画
		isVisible = true;
	});

	// 监听路由变化
	$effect(() => {
		if ($page.url.pathname) {
			isVisible = false;
			setTimeout(() => {
				isVisible = true;
			}, 50);
		}
	});
</script>

<div
	class="page-transition-container {className}"
	class:animate-fade-in={isVisible}
>
	{@render children?.()}
</div>

<style>
	.page-transition-container {
		opacity: 0;
		transform: translateY(20px);
		transition: opacity 0.3s var(--ease-out), transform 0.3s var(--ease-out);
	}

	.page-transition-container.animate-fade-in {
		opacity: 1;
		transform: translateY(0);
	}
</style>