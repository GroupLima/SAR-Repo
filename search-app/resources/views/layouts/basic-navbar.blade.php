<!-- resources/views/layouts/basic-navbar.blade.php -->

<!-- this can be changed later on by the sass team -->
<nav id="navbar" class="navbar">
    <div class="nav-content">
        <div class="logo-section" onclick="navigateToPage('/home');">

            <div class="text-container"> <!-- New container for text -->
                <div class="logo-text">SAR</div>
                <div class="logo-subtext">Search Aberdeen Registers</div>
            </div>
            <img src="{{ asset('images/town.png') }}" alt="Town Logo" class="logo-image">
        </div>
        <div class="nav-links">
            <a href="/home" onclick="navigateToPage('/home'); return false;">Home</a>
            <a href="/browse" onclick="navigateToPage('/browse'); return false;">Browse</a>
            <a href="/xquery" onclick="navigateToPage('/xquery'); return false;">XQuery</a>
            <a href="/about" onclick="navigateToPage('/about'); return false;">About</a>
        </div>
    </div>
</nav>
<script>
    // Function to transition to a new page with fade-out effect
    function navigateToPage(url) {
        // Fade out the body
        document.querySelector('body').style.opacity = 0;

        // After 500ms (duration of the fade-out), navigate to the new page
        setTimeout(function() {
            window.location.href = url;
        }, 500); // This timeout should match the fade-out duration
    }

    // When the page is fully loaded, fade it in
    window.addEventListener("load", (event) => {
        // Fade in the body
        document.querySelector('body').style.opacity = 1;
    });
</script>
