<script>
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import Slider from "@bulatdashiev/svelte-slider";
    import MultiSelect from './MultiSelect.svelte';
    import { palette } from "$lib/data/palette";
    import { Modal, ModalContent, Tooltip } from "$lib/components";
    import {
        UN_class_1,
        UN_class_3,
        UN_class_4_1,
        UN_class_4_2,
        UN_class_4_3,
        UN_class_5_1,
        UN_class_5_2,
        UN_class_6_1,
        UN_class_6_2,
        UN_class_8,
        UN_class_9,
    } from "$lib/svg";


    export let select_options_in = [];

    const svg_w = 55;

    const levels = ["country", "sub_region", "region", "hdi"];
    const levels_label = ["Country", "Subregion", "Region", "HDI"];
    let level = [3, 4];
    if ($page.url.searchParams.get("level") !== null) {
        level = [levels.indexOf($page.url.searchParams.get("level")) + 1, 4];
    }

    let selection = "all";
    if (level[0] == 1) {
        selection = "af";
    }
    if ($page.url.searchParams.get("selection") !== null) {
        selection = $page.url.searchParams.get("selection");
    }

    let years = [2001, 2021];
    if ($page.url.searchParams.get("years") !== null) {
        let y = JSON.parse(`[${$page.url.searchParams.get("years")}]`);
        years[0] = y[0];
        years[1] = y[1];
    }

    let per_capita = false;
    if ($page.url.searchParams.get("per_capita") !== null) {
        per_capita = JSON.parse($page.url.searchParams.get("per_capita"));
    }

    let select_options = [];
    $: select_options = select_options_in[level[0] - 1];    

    let categories = ["all"];

    function handleSelected(s){
        if (categories.includes(s)){
            console.log("selected")
            return "selected"
            
        }
        else{return ""}
    }

    if ($page.url.searchParams.get("categories") !== null) {
        
        categories = $page.url.searchParams.get("categories")?.split(",");
       
    }

   $:console.log(categories)
    let range;
    let showModal = false;

    async function set_url() {
        const url = $page.url.searchParams;
        url.set("selection", selection);
        url.set("per_capita", per_capita);
        url.set("years", years);
        url.set("level", levels[level[0] - 1]);
        url.set("categories", categories);
        await goto(`?${url}`, { invalidateAll: true });
    }

    const components = {
        UN_class_1,
        UN_class_3,
        UN_class_4_1,
        UN_class_4_2,
        UN_class_4_3,
        UN_class_5_1,
        UN_class_5_2,
        UN_class_6_1,
        UN_class_6_2,
        UN_class_8,
        UN_class_9,
    };
</script>

<div class="p-3 ">
    <div class="mb-3 border-b">
        <h1 class="font-bold text-3xl pb-4">Basel Viz</h1>
        <p class="pb-3">
            Visualizing country reports under the Basel Convention on the
            Control of Transboundary Movements of Hazardous Wastes and Their
            Disposal.
        </p>
        <button
            class="font-medium text-blue-600 dark:text-blue-500 hover:underline pb-3"
            on:click={() => (showModal = true)}
        >
            More Information
        </button>
    </div>

    <div class="border-b mb-3">
        <h1 class="font-bold text-lg pb-4">Filter Options</h1>
        <!-- Level Slider-->
        <div class="pb-4 flex items-center">
            <p class="">Level:</p>
            <div class=" px-8 w-3/4">
                <Slider
                    min={1}
                    max={4}
                    step="1"
                    bind:value={level}
                    on:input={() => {
                        level[0] != 1 ? (selection = "all") : (selection = "af");
                    }}
                >
                    <div slot="left" class="bg-white">
                        <span
                            class="mb-2 border rounded-full py-1 px-3 "
                            style="font-size: 14px;"
                            >{levels_label[level[0] - 1]}</span
                        >
                    </div>
                </Slider>
            </div>
        </div>
        <!-- Country Dropdown -->
        <div class="pb-4">
            <label class="pr-3" for="select">Select:</label>
            <select
                class="px-3 w-2/4"
                name="country"
                id="select"
                bind:value={selection}
            >
                <option selection value="all">All</option>
                {#if select_options}
                    {#each Object.entries(select_options) as option}
                        <option value={option[0]}>{option[1].name}</option>
                    {/each}
                {/if}
            </select>
        </div>
        <!-- Time Range Slider-->
        <div class="pb-4">
            <p class="pb-3">Time Range:</p>
            <div class=" px-6">
                <Slider min={2001} max={2021} step="1" bind:value={years} range>
                    <div slot="left" class="bg-white">
                        <span class="mb-2 border rounded-full py-1 px-3 "
                            >{years[0]}</span
                        >
                    </div>
                    <div slot="right" class="bg-white">
                        <span class="mb-2 border rounded-full py-1 px-3 "
                            >{years[1]}</span
                        >
                    </div>
                </Slider>
            </div>
        </div>
        <!-- Categories Dropdown-->

        <MultiSelect  bind:value={categories}>
            <option selected={`${handleSelected("all")}`} value="all">All</option>
            <option selected={`${handleSelected("1")}`} value="1">Class 1</option>
            <option selected={`${handleSelected("3")}` } value="3">Class 3</option>
            <option selected={`${handleSelected("4_1")}`} value="4_1">Class 4.1</option>
            <option selected={`${handleSelected("4_2")}`} value="4_2">Class 4.2</option>
            <option selected={`${handleSelected("4_3")}`} value="4_3">Class 4.3</option>
            <option selected={`${handleSelected("5_1")}`} value="5_1">Class 5.1</option>
            <option selected={`${handleSelected("5_2")}`} value="5_2">Class 5.2</option>
            <option selected={`${handleSelected("6_1")}`} value="6_1">Class 6.1</option>
            <option selected={`${handleSelected("6_2")}`} value="6_2">Class 6.2</option>
            <option selected={`${handleSelected("8")}`} value="8">Class 8</option>
            <option selected={`${handleSelected("9")}`} value="9">Class 9</option>
            <option selected={`${handleSelected("unknown")}`} value="unspecified">Class Unknown</option>
            <option selected={`${handleSelected("multiple")}`} value="multiple">Multiple Classes</option>
        </MultiSelect>
       
        <!-- per_capita Checkbox -->
        <div class="pb-4 flex items-center">
            <label class="pr-2">
                <input class="mr-1" type="checkbox" bind:checked={per_capita} />
                <span>Per capita</span>
            </label>
            <Tooltip>Amount divided by population</Tooltip>
        </div>

        <button
            class="border rounded py-1 px-3 bg-neutral-200 mb-6"
            on:click={set_url}>Submit</button
        >
    </div>
    <div class="">
        <h1 class="font-bold text-lg pb-3">Legend</h1>
        <h2 class="font-medium text-base pb-6">Waste Categories:</h2>
        <div class="grid grid-cols-2 mb-3 gap-y-5 gap-x-1">
            {#each palette.description as description, i}
                <div class="flex space-x-4 text-sm items-center">
                    <div
                        class=""
                        style="background-color: {palette.colors[
                            i
                        ]}; min-height: {svg_w}px; min-width: {svg_w}px;"
                    >
                        {#if palette.svgs[i] != ""}
                            <svelte:component
                                this={components[`UN_class_${palette.svgs[i]}`]}
                                width={svg_w}
                                height={svg_w}
                            />
                        {:else}{/if}
                    </div>
                    {#if palette.class_written[i] != ""}
                        <span
                            ><span class="font-semibold"
                                >{palette.class_written[i]}</span
                            >
                            : <br />
                            {description}</span
                        >
                    {:else}
                        <span>{description}</span>
                    {/if}
                    <div />
                </div>
            {/each}
        </div>
    </div>
</div>
<!-- Modal Content -->
<Modal bind:showModal>
    <ModalContent />
</Modal>
