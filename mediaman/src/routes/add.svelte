<script lang="ts">
	import api from '$lib/api';
	import type { Channel } from '$lib/types';
	import { prettyNum } from '$lib/utils';
	import { onMount } from 'svelte';

	let id: string = '';
	let channel: Channel | null = null;

	const handleSearch = async () => {
		const response = await api.putChannel(id);
		channel = response.data;
	};

	const handleFollow = async () => {
		const result = await api.changeFollow(id);
		if (channel) {
			channel.following = result.data;
		}
	};
</script>

<article>
	<section class="form-control">
		<div class="input-group">
			<input
				type="text"
				placeholder="Search channel by id..."
				class="input input-bordered"
				bind:value={id}
			/>
			<button class="btn btn-square" on:click={handleSearch}>Search</button>
		</div>
	</section>

	{#if channel}
		<section class="channel">
			<div class="banner">
				<img src={channel.banner} alt={`Banner for ${channel.title}`} />
			</div>
			<div class="channel-info">
				<div class="name-group">
					<img src={channel.avatars[0].url} alt="Avatar" class="avatar" />
					<div class="name">
						<h2>{channel.title}</h2>
						<div class="info">{prettyNum(channel.subscribers)} subscribers</div>
						<div class="info">{prettyNum(channel.videos)} videos</div>
					</div>
				</div>
				<button class="btn" on:click={handleFollow}
					>{channel.following ? 'Following' : 'Follow'}</button
				>
			</div>
			<p>{channel.description}</p>
		</section>
	{/if}
</article>

<style>
	.input-group {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	input[type='text'] {
		width: 40%;
	}

	button {
		width: fit-content;
		padding: 1rem;
	}

	.channel {
		margin: 1rem 0;
	}

	.banner {
		width: 100%;
		height: 200px;
		overflow: hidden;
	}

	.banner img {
		width: 100%;
		transform: translateY(-40%);
	}

	.channel-info {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin: 0 1rem;
	}

	.name-group {
		display: flex;
		align-items: center;
		margin: 1rem 0;
	}

	.avatar {
		border-radius: 50%;
		margin: 0 1rem 0 0;
	}

	.name h2 {
		margin: 0;
	}

	.info {
		font-size: 0.9rem;
	}

	p {
		margin: 0 1rem;
	}
</style>
