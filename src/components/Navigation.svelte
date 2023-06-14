<script>

let expanded = false;
function handleToggle() {
    expanded = !expanded;
}

</script>

<div class="hamburger" on:click={handleToggle} on:keyup={handleToggle}>
    <span class="line"></span>
    <span class="line"></span>
    <span class="line"></span>
</div>

<div class="grow">
    <div class="nav-links" class:expanded="{expanded}">
        <a href="/">Home</a>
        <a href="/about/">About</a>
        <a href="/blog/">Blog</a>
        <a href="/tags/">Tags</a>
    </div>
</div>