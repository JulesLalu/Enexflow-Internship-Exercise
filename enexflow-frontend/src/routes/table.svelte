<script>
  export let promise;
</script>

{#await promise}
<p>Loading...</p>
{:then promise}
<table class="table">
  <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">Date</th>
      <th scope="col">Conso</th>
    </tr>
  </thead>
  <tbody>
    {#each promise as datapoint,j}	
      <tr>
        <th scope="row">{j}</th>
        <td>{datapoint.date}</td>
        <td>{datapoint.conso} MWh</td>
      </tr>
    {/each}
  </tbody>
</table>
{:catch error}
<p style="color: red">{error.message}</p>
{/await}
