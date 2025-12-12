<script>
	export let type = 'fadeIn';
	export let duration = 300;
	export let delay = 0;
	export let repeat = false;
	export let hover = false;

	const animationMap = {
		fadeIn: 'fadeIn',
		slideUp: 'slideInUp',
		slideDown: 'slideInDown',
		slideLeft: 'slideInLeft',
		slideRight: 'slideInRight',
		scaleIn: 'scaleIn',
		bounceIn: 'bounceIn',
		pulse: 'pulse',
		float: 'cardFloat'
	};

	const animationClass = $derived(animationMap[type] || type);
	const durationClass = $derived(`duration-${duration}`);
	const delayClass = $derived(delay > 0 ? `delay-${delay}` : '');
</script>

<div
	class="animate-{animationClass} {durationClass} {delayClass}"
	class:repeat={repeat}
	class:hover-float={hover}
>
	<slot />
</div>