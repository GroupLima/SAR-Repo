<!-- resources/views/layouts/basic-navbar.blade.php -->

<!-- this can be changed later on by the sass team -->
<nav id="navbar" class="navbar">    
    <div class="nav-content">
        <div class="logo-section">

            <div class="text-container"> <!-- New container for text -->    
                <div class="logo-text">SAR</div>
                <div class="logo-subtext">Search Aberdeen Registers</div>
            </div>
            <img src="{{ asset('images/logo-current-thin.png') }}" alt="Town Logo" style = "width: 110px; height: 110px;">
        </div>
        <div class="nav-links">
            <a href='/home'>Home</a>
            <a href='/browse'>Browse</a>
            <a href='/xquery'>XQuery</a>
            <a href='/about'>About</a>
        </div>
    </div>
</nav>