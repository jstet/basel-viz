<script>
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import Slider from "@bulatdashiev/svelte-slider";
    import { palette } from "$lib/data/palette";
    import Modal from "$lib/components/Modal.svelte";
    import UN_class_1 from "$lib/svg/UN_class_1.svelte";
    import UN_class_3 from "$lib/svg/UN_class_3.svelte";
    import UN_class_4_1 from "$lib/svg/UN_class_4_1.svelte";
    import UN_class_4_2 from "$lib/svg/UN_class_4_2.svelte";
    import UN_class_4_3 from "$lib/svg/UN_class_4_3.svelte";
    import UN_class_5_1 from "$lib/svg/UN_class_5_1.svelte";
    import UN_class_5_2 from "$lib/svg/UN_class_5_2.svelte";
    import UN_class_6_1 from "$lib/svg/UN_class_6_1.svelte";
    import UN_class_6_2 from "$lib/svg/UN_class_6_2.svelte";
    import UN_class_8 from "$lib/svg/UN_class_8.svelte";
    import UN_class_9 from "$lib/svg/UN_class_9.svelte";

    export let select_options_in = [];

    const levels = ["country", "sub_region", "region"];
    const levels_label = ["Country", "Sub Region", "Region"];
    let level = [3, 3];
    if ($page.url.searchParams.get("level") !== "undefined"){
        level = [levels.indexOf($page.url.searchParams.get("level"))+1,3]
    }
    
    let selected;
    if ($page.url.searchParams.get("selected") !== "undefined"){
        selected = $page.url.searchParams.get("selected");
    }
    

    let years = [2001, 2021];
    if ($page.url.searchParams.get("years") !== "undefined"){
        let y = JSON.parse(`[${$page.url.searchParams.get("years")}]`)
        years[0] = y[0]
        years[1] = y[1]
    }

    let normalize = false;
    
    

    let select_options = []
    $: select_options = select_options_in[level[0]-1]

    let range;
    let showModal = false;

    async function set_url() {
        const url = $page.url.searchParams;
        url.set("selected", selected);
        url.set("normalize", normalize);
        url.set("years", years);
        url.set("level", levels[level[0]-1]);
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
        <div class="pb-3 flex items-center">
            <p class="">Level:</p>
            <div class=" px-6 w-2/4">
                <Slider min={1} max={3} step="1" bind:value={level} on:input={()=>{selected="all"}}>
                    <div slot="left" class="bg-white">
                        <span
                            class="mb-2 border rounded-full py-1 px-3 "
                            style="font-size: 20px;">{level[0]}</span
                        >
                    </div>
                </Slider>
            </div>
        </div>
        <!-- Dropdown -->
        <div class="pb-3">
            <label class="pr-3" for="select">Select:</label>
            <select
                class="px-3 w-2/4"
                name="country"
                id="select"
                bind:value={selected}

            >
                <option selected value="all">All</option>
                {#if select_options}
                    {#each Object.entries(select_options) as option}
                        <option value={option[0]}>{option[1].name}</option>
                    {/each}
                {/if}
            </select>
        </div>
        <!-- Time Range Slider-->
        <div class="pb-3">
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
        <!-- Normalize Checkbox -->
        <div class="pb-3">
            <label>
                <input type="checkbox" bind:checked={normalize} />
                Normalize
            </label>
        </div>
        <button
            class="border rounded py-1 px-3 bg-neutral-200 mb-6"
            on:click={set_url}>Submit</button
        >
    </div>
    <div class="border-b">
        <h1 class="font-bold text-lg pb-4">Legend</h1>
        <div class="grid grid-cols-2 gap-5 mb-3">
            {#each palette.description as description, i}
                <div class="flex space-x-4 text-sm items-center">
                    <div
                        class="h-16 w-16"
                        style="background-color: {palette.colors[i]};"
                    >
                        {#if palette.svgs[i] != ""}
                            <svelte:component
                                this={components[`UN_class_${palette.svgs[i]}`]}
                                width={64}
                                height={64}
                            />
                        {:else}{/if}
                    </div>
                    {#if palette.class_written[i] != ""}
                        <span
                            ><span class="font-bold"
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
    <p class="font-light absolute bottom-0 pb-3">
        Created by Xenia Saar, Freya Moßig and Jonas Stettner
    </p>
</div>
<!-- Modal Content -->
<Modal bind:showModal>
    <h2 class="font-bold text-3xl pb-4">Basel Viz</h2>

    <h3 class="pb-3">Article 13.3 of the Basel Convention states:</h3>
    <blockquote class="italic">
        <p class="pb-1">
            "The Parties, [...] shall transmit, [...] before the end of each
            calendar year, a report on the previous calendar year, containing
            the following information:
        </p>

        <p class="pb-1 pl-4">
            (b) Information regarding transboundary movements of hazardous
            wastes or other wastes in which they have been involved, including:
        </p>
        <p class="pb-3 pl-10">
            (ii) The amount of hazardous wastes and other wastes imported their
            category, characteristics, origin, and disposal methods;"
        </p>
    </blockquote>
    <p class="pb-10">
        The data contained in these reports is publically available and was
        scraped and aggregated for this visualization.
    </p>
    <p class="pb-10">
        <a
            href="http://www.basel.int/"
            class="font-medium text-blue-600 dark:text-blue-500 hover:underline"
            >Read more</a
        >
    </p>
    <p /></Modal
>
