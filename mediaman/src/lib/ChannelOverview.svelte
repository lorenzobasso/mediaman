<script lang="ts">
	import type { Channel } from './types';

	export let channel: Channel;

	$: avatar = channel.avatars.find((a) => a.size === 'high') ?? channel.avatars[0];
</script>

<img src={avatar.url} alt={avatar.size} />

<style>
	img {
		width: 100%;
		border-radius: 2rem;
	}

	img:hover {
		width: calc(100% - 2px);
		padding: 2px;
		cursor: pointer;
	}
</style>
