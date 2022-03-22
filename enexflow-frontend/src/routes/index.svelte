<script lang="ts">
	import Label from './label_home.svelte'
	import Table from './table.svelte'
	import {mystore, getjson, updatedb} from './types'
//que pour les composants sveltes sans accolades
//fonctions peuvent être mis dans des fichiers aussi

	let i=0;
	let displayresults=false;	
	let displayanswer=false;

	function displayData() : void {
		mystore.set({promise1: getjson(i)}); //on met à jour la valeur
		displayresults = true;
	}

	function update_done() : void{
		mystore.set({promise2: updatedb()});
		displayanswer=true;
	}
</script>


<p class = "bd-lead">Please choose the time duration used for displaying consumption data</p>

<div class="container">
	<Label bind:i={i} displayData={displayData}/>	

	{#if displayresults}
		<Table promise={$mystore.promise1}/>
	{/if}

		<footer>
			<button on:click={update_done} class="btn btn-outline-primary">Update database</button>
			{#if displayanswer}
				{#await $mystore.promise2}
					<p class = "mt-0">Loading...</p>
				{:then promise}
				{#each promise as msg}	
					<p class = "mt-0">{msg.state}</p>
				{/each}
				{/await}
			{/if}
		</footer>


</div>

<style>
	.bd-lead{
		margin-left: 0.65rem;
		font-size: large;
		color: rgba(0, 0, 0, 0.808);
		padding-bottom: 1.5%;
	}

	.mt-0 {
		margin-top: 1em !important;
	}

	div{
		margin: 0 auto;
	}

	footer{
		padding-top: 4%;
	}

</style>
