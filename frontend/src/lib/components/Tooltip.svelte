<script>
    import { Info } from "$lib/svg";

    let visible = true;

    function handleMouseOver(e) {
        visible = true;
    }
    function handleMouseOut(e) {
        visible = false;
    }
</script>

<div on:mouseover={handleMouseOver} on:mouseout={handleMouseOut} class="z-10 ">
    <div>
        <Info height={20} width={20} />
    </div>
</div>

{#if visible}
<div class="flex h-5">
    <div class="relative w-64 h-full flex items-center">
        <div class="pl-2 absolute">
            <slot />
        </div>
    </div>
</div>
{/if}
