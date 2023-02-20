<script>
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import Slider from "@bulatdashiev/svelte-slider";
    let selected;
    let value = [2001, 2021];
    let range;
    let normalize = false;

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
    <div class="mb-5">
        <h1 class="font-bold text-2xl">Basel Viz</h1>
        <p>Visualizing hazardous waste routes</p>
    </div>
    <div>
        <div class="pb-14">
            <label for="country">Choose a country:</label>
            <select name="country" id="country" bind:value={selected}>
                <option selected value="all">All</option>
                <option value="de">Germany</option>
                <option value="fr">France</option>
            </select>
        </div>
        <div class="mb-6 px-6">
            <Slider min={2001} max={2021} step="1" bind:value range>
                <div slot="left" class="h-24">
                    <span
                    class="mb-2 border rounded-full py-1 px-3 "
                    
                    >{value[0]}</span
                >
                </div>
                <div slot="right" class="h-24">
                    <span
                    class="mb-2 border rounded-full py-1 px-3 "
                    
                    >{value[1]}</span
                >
                </div>
                
            </Slider>
        </div>

        <div>
            <label>
                <input type="checkbox" bind:checked={normalize} />
                Normalize
            </label>
        </div>
        <button
            class="border rounded py-1 px-3 bg-neutral-200"
            on:click={set_url}>Submit</button
        >
    </div>
</div>
