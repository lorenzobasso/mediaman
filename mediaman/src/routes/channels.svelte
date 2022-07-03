<script lang="ts">
	import api from '$lib/api';
	import ChannelOverview from '$lib/ChannelOverview.svelte';

	import type { Channel } from '$lib/types';

	import { onMount } from 'svelte';

	let channels: Channel[] = [];

	onMount(async () => {
		const response = await api.getFollowed();
		channels = response.data;
	});
</script>

<article>
	{#each channels as channel}
		<ChannelOverview {channel} />
	{/each}
</article>

<style>
	article {
		display: grid;
		grid-template-columns: repeat(5, 1fr);
		gap: 1rem;
	}
</style>
