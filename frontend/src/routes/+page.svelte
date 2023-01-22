<script>
    import Map from "$lib/components/Map.svelte";
    import Sidepanel from "$lib/components/Sidepanel.svelte";
    export let data;
</script>

<div class="flex w-screen h-screen">
    <div class="w-1/5 border-r border-neutral-400 z-10"><Sidepanel /></div>
    <div class="w-4/5 h-100"><Map /></div>
</div>
