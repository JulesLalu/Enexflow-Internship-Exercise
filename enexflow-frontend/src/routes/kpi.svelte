<script lang="ts">
    import {mystore, kpi_cons, mean_per_hour} from './types'

//factoriser, mettre dans fichier ts
//store : endroit où on va stocker de l'info qui va être dispo partout
//si on est dans une route, on va mettre à jour la valeur dans cette route et ça va être maj dans les autres routes
</script>

<p class = "bd-lead">Here are the KPIs corresponding to the fetched data</p>

<div class="container">	
    {#await $mystore.promise1}
    <p>Loading</p>
    {:then promise}
	<div id="parent">
		<div class="text-start">Mean consumption : </div>
	</div>
    {/await}
</div>

<style>
	.bd-lead{
		margin-left: 1rem;
		font-size: large;
		color: rgba(0, 0, 0, 0.808);
		padding-bottom: 1.5%;
	}

	.text-start{
		margin-left: 0.3rem;
		display : inline-block;
		font-size: large;
		color: chocolate;
	}

	.p-2{
		margin-left: 1.3rem;
		padding: 0rem!important;
		display : inline-block;
		font-size: 105%;
	}

	div{
		margin: 0 auto;
	}
</style>
