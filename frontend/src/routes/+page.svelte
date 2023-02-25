<script>
    import Map from "$lib/components/Map.svelte";
    import Sidepanel from "$lib/components/Sidepanel.svelte";
    export let data;
    let flows;
    $: flows = data.flows
    let points;
    $: points = data.points
    let coords;
    $: coords = data.coords
    let countries;
    $: countries = data.countries
   
</script>

<div class="flex w-screen h-screen">
    <div class="w-1/5 border-r border-neutral-400 z-10 overflow-scroll" countries={countries}><Sidepanel /></div>
    <div class="w-4/5 h-100"><Map flows={flows} points={points} /></div>
</div>
