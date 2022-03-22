import {writable} from 'svelte/store'
type Promise_dict = {
    promise1?: Promise<Datapoint[]>
    promise2?: Promise<State[]>
};

export const mystore = writable<Promise_dict>({promise1: undefined, promise2: undefined}); //store writable dans lequel je stocke une donnée promise<dp>
//mystore n'est pas modifié, c'est juste ce qui est à l'intérieur qui est modifié

export type State = {
    state : string;
};

export type Datapoint = {
    date : string;
    conso : number;
}

export async function getjson(number: number): Promise<Datapoint[]> {
    let response = await fetch("http://localhost:5000/electricity_consumption?n="+String(number));
    return await response.json();
}

export async function updatedb() : Promise<State[]> {
    let response = await fetch("http://localhost:5000/refresh_conso")
    return await response.json();
}

function mean(ConsoArray: number[]): number {
    let sum = 0;
    for (let i = 0; i < ConsoArray.length; i++) {
        sum += ConsoArray[i];
    }
    sum/=ConsoArray.length;
    return sum
}

function Datapt_to_number(DataptArray: Datapoint[]): number[] {
    let numb_array: number[] = [];
    for (let i = 0; i < DataptArray.length; i++) {  
        numb_array.push(DataptArray[i].conso) ;
    }
    return numb_array
}

export function kpi_cons(DataptArray: Datapoint[]): number {
    return Math.round(mean(Datapt_to_number(DataptArray))*100)/100
}

export function mean_per_hour(DataptArray: Datapoint[]): Datapoint[] {
    const set1: Set<string> = new Set();
    for (let i = 0; i < DataptArray.length; i++) {
        let str= DataptArray[i].date
        set1.add(str.substring(0, 14)+'00')
    }
    let hour_array: Array<string> = Array.from(set1)
    let datapt_mean: Datapoint[] = []  
    for (let i = 0; i < hour_array.length; i++) {
        datapt_mean.push({date:hour_array[i],conso:0})
    }
    for (let k in DataptArray){
    }
    return datapt_mean
}
// create Datapoint[]
// while last 2 char différents de 00 : sum+= conso
// initial date.conso = sum
// for i in ... 
// time.conso = Array[3i] + Array[3i+1] + Array[3i+2] + Array[3i+3] 