<script lang="ts">
  import type Match from './Match.svelte';
  import { splitMatchParts } from './matchHighlighterUtils';
  import PrecomputedMatchHighlighter from './PrecomputedMatchHighlighter.svelte';

  export let text: string;
  export let substring = '';
  export let matchComponent: typeof Match | undefined = undefined;

  $: matchParts = splitMatchParts(text, substring);
</script>

<PrecomputedMatchHighlighter {matchParts} {matchComponent} />
