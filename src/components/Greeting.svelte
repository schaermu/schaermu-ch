<script>
    export let messages = [];
    let greeting = ''

    function handleGreetClick()  {
        greeting = messages[Math.floor(Math.random() * messages.length)];
    }
    
    handleGreetClick();
</script>

<div> 
    <h3>{greeting}! Thank you for visiting!</h3>
    <button on:click={handleGreetClick}>
        New Greeting
    </button>
</div>