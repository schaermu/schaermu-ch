<script>

let expanded = false;

</script>

<div class="hamburger" on:click={() => expanded = !expanded}>
    <span class="line"></span>
    <span class="line"></span>
    <span class="line"></span>
</div>

<div class="nav-links" class:expanded="{expanded}">
    <a href="/">Home</a>
    <a href="/about/">About</a>
    <a href="/blog/">Blog</a>
    <a href="/tags/">Tags</a>
</div>