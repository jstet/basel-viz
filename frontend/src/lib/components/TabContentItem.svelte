<script lang="ts">
    export let activeTabValue;
    export let id;
   
  </script>
  
  {#if activeTabValue === id}
    <div class="h-full w-full" id="{id}-tabitem" role="tabpanel" aria-labelledby="{id}-tab">
      <slot />
    </div>
  {/if}