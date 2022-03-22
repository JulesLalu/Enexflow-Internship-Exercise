<script lang='ts'>
    export let i=0;
    export let displayData: () => void; //pour des callbacks, on va utiliser des conventions on:click={nom_bouton} (ici showresults)
</script>
 
<div class="input-group mb-3">
    <div class="input-group-prepend">
      <span class="input-group-text" id="basic-addon1">Number of hours</span>
    </div>
    <input type="text" class="form-control" bind:value={i}>
    <input type="range" class="form-range" min="0" max="48" bind:value={i} id="hours_range">
    <button on:click={displayData} class="btn btn-outline-secondary" type="button" id="button-addon2">Show results</button>
</div>

<h2>
    Data granularity : 15 min
</h2>	


<style>
    .form-control{
        flex: 1 1 auto;
        width : 5%;
    }
    .form-range{
        padding : 20px;
        width : 50%;
    }
</style>