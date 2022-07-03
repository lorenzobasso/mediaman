<script lang="ts">
	import '../app.css';
</script>

<header>
	<a href="/">
		<h1>Mediaman</h1>
	</a>
	<nav>
		<a href="/add">Add channel</a>
		<a href="/channels">Channels</a>
	</nav>
</header>

<main><slot /></main>

<style>
	header {
		height: var(--header-height);
		display: flex;
		justify-content: space-between;
		align-items: end;
		padding: 0.2rem 1rem 0.2rem;
		margin: 0 0 1rem;
		border-bottom: 2px solid hsl(var(--b3));
	}

	h1 {
		margin: 0;
	}

	nav {
		display: flex;
	}

	nav > a {
		text-decoration: none;
		text-transform: uppercase;
		margin-right: 1rem;
	}

	nav > a:hover {
		text-decoration: underline;
	}

	nav > a:last-of-type {
		margin-right: 0;
	}

	a {
		text-decoration: none;
	}

	main {
		margin: 1rem 0;
		height: calc(100vh - 2rem - var(--header-height));
	}
</style>
