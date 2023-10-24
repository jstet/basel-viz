<script>
    export let id;
    export let activeTabValue;
  </script>
  
  <li class="" role="presentation">
    <button
      on:click
      class="w-40 p-4 active bg-white border-t border-neutral-400 font-medium 
      {id == 1 ? "border-l" : "border-r"} 
      {id == 1 ? "rounded-tl-lg" : "rounded-tr-lg"}
      {activeTabValue == id ? "bg-gray-300 " : "bg-none"}"
      id="{id}-tabhead"
      type="button"
      role="tab">
      <slot />
    </button>
  </li>