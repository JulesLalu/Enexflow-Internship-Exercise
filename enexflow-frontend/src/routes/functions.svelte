<script lang="ts" context="module">
    export let promise: Promise<Datapoint[]|State[]>;
    type State = { 
		state : string;
	}

	type Datapoint = {
		date : string;
		conso : number;
	}
	
    async function getjson(number : number) : Promise<Datapoint[]> {
        let response = await fetch("http://localhost:5000/electricity_consumption?n="+String(number));
        return await response.json();
    }

    async function updatedb() : Promise<State[]> {
        let response = await fetch("http://localhost:5000/refresh_conso")
        return await response.json();
    }

    function displayData (api_call : (num?: number)=> Promise<Datapoint[]|State[]>) {
        if (num !== undefined) {
            promise = api_call(num);
            displayresults = true;
        }
        else {
            promise = api_call();
            displayupdate = true;
        }
    }
</script>