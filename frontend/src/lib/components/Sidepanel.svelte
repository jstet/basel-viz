<script>
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import Slider from "@bulatdashiev/svelte-slider";
    import { palette } from "$lib/data/palette";
    import Modal from "$lib/components/Modal.svelte";
    let selected;
    let value = [2001, 2021];
    let range;
    let normalize = false;
    let showModal = false;

    async function set_url() {
        const url = $page.url.searchParams;
        url.set("country", selected);
        url.set("normalize", normalize);
        url.set("year", value);
        await goto(`?${url}`, { invalidateAll: true });
    }
</script>

<!-- SUBMIT BUTTON-->
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
        <div class="pb-3">
            <label class="pr-3" for="country">Country:</label>
            <select
                class="px-3"
                name="country"
                id="country"
                bind:value={selected}
            >
                <option selected value="all">All</option>
                <option value="de">Germany</option>
                <option value="fr">France</option>
            </select>
        </div>
        <div class="pb-3">
            <p class="pb-3">Time Range:</p>
            <div class=" px-6">
                <Slider min={2001} max={2021} step="1" bind:value range>
                    <div slot="left" class="bg-white">
                        <span class="mb-2 border rounded-full py-1 px-3 "
                            >{value[0]}</span
                        >
                    </div>
                    <div slot="right" class="bg-white">
                        <span class="mb-2 border rounded-full py-1 px-3 "
                            >{value[1]}</span
                        >
                    </div>
                </Slider>
            </div>
        </div>

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
        {#each palette.labels as label,i}
        <div class="flex space-x-4">
        <div class="h-10 w-10 mb-3" style="background-color: {palette.colors[i]};"></div>
        <span>{label}</span>
    </div>
        {/each}
    </div>
    <p class="font-light absolute bottom-0 pb-3">
        Created by Xenia Saar, Freya Moßig and Jonas Stettner
    </p>
</div>

<Modal bind:showModal>
    <h2 class="font-bold text-3xl pb-4">Basel Viz</h2>

    <h3 class="pb-3">Article 13.3 of the Basel Convention states:</h3>
    <blockquote
        class="italic"
    >
        
        <p class="pb-1">
            "The Parties, [...] shall
            transmit, [...] before the end of each calendar year,
            a report on the previous calendar year, containing the following
            information:
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
    <p class="pb-10">The data contained in these reports is publically available and was scraped and aggregated for this visualization.</p>
    
</Modal>
