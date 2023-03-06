<script>
    import {
        TabWrapper,
        TabHead,
        TabHeadItem,
        TabContentItem,
        Map,
        Sidepanel,
        ChordDia
    } from "$lib/components";
    export let data;
    let flows;
    $: flows = data.flows;
    let points;
    $: points = data.points;
    let coords;
    $: coords = data.coords;
    let select_options;
    $: select_options = data.select_options;
    let no_exports;
    $: no_exports = data.no_exports;
    let activeTabValue = 1;
    const handleClick = (tabValue) => () => {
        activeTabValue = tabValue;
    };
</script>

<div class="flex w-screen h-screen">
    <div class="2xl:w-3/12 xl:w-4/12 w-2/5 border-r border-neutral-400 z-10 overflow-scroll">
        <Sidepanel select_options_in={select_options} />
    </div>
    <div class="2xl:w-9/12 xl:w-8/12 w-3/5 h-full relative">
        <TabWrapper>
            <TabContentItem id={1} {activeTabValue}>
                <Map {flows} {points} {coords} {no_exports} />
            </TabContentItem>
            <TabContentItem id={2} {activeTabValue}>
                <ChordDia {flows} {points} {no_exports} />
            </TabContentItem>
        </TabWrapper>
    </div>
    <TabHead>
        <TabHeadItem id={1} {activeTabValue} on:click={handleClick(1)}
            >Map</TabHeadItem
        >
        <TabHeadItem id={2} {activeTabValue} on:click={handleClick(2)}
            >Chord Diagram</TabHeadItem
        >
    </TabHead>
</div>
