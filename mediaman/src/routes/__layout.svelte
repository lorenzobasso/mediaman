<script lang="ts">
	import '../app.css';
</script>

<header>
	<h1>Mediaman</h1>
	<nav>cya</nav>
</header>

<main><slot /></main>

<style>
	header {
		background-color: red;
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0 1rem;
	}

	h1 {
		margin: 0;
	}
</style>
