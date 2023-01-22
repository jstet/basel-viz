<script>
    let selected;
    let normalize = false;
    $: console.log(normalize);
</script>

<div class="p-3 ">
    <div class="mb-5">
        <h1 class="font-bold text-2xl">Basel Viz</h1>
        <p>Visualizing hazardous waste routes</p>
    </div>
    <div>
        <div class="mb-2">
            <label for="country">Choose a country:</label>
            <select name="country" id="country" bind:value={selected}>
                <option selected value="Germany">All</option>
                <option value="Germany">Germany</option>
                <option value="France">France</option>
            </select>
        </div>

        <div>
            <label>
                <input type=checkbox bind:checked={normalize}>
                Normalize
            </label>
        </div>
    </div>
</div>
