<script>
    import { goto } from '$app/navigation'
    import { page } from '$app/stores'
    let selected;
    let normalize = false;

    async function set_url() {
        const url = $page.url.searchParams;
        url.set("country", selected);
        url.set("normalize", normalize)
        await goto(`?${url}`, {invalidateAll: true});
    }
</script>

<div class="p-3 ">
    <div class="mb-5">
        <h1 class="font-bold text-2xl">Basel Viz</h1>
        <p>Visualizing hazardous waste routes</p>
    </div>
    <div>
        <div class="mb-2">
            <label for="country">Choose a country:</label>
            <select name="country" id="country" bind:value={selected} on:change={set_url}>
                <option selected value="all">All</option>
                <option value="de">Germany</option>
                <option value="fr">France</option>
            </select>
        </div>

        <div>
            <label>
                <input type="checkbox" bind:checked={normalize} on:change={set_url}/>
                Normalize
            </label>
        </div>
    </div>
</div>
