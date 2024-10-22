<!-- resources/views/layouts/basic-navbar.blade.php -->

<!-- this can be changed later on by the sass team -->
<div>
    <ul>
        <li><a href='/home'>Home</a></li>
        <li><a href='/search'>Search</a></li>
        <li><a href='/browse'>Browse</a></li>
        <li><a href='/xquery'>XQuery</a></li>
        <li><a href='/about'>About</a></li>
    </ul>
    <style>
        ul {
            padding: 0;
            margin: 0;
            list-style-type: none; /* Remove default bullet points */
        }
        li {
            display: inline;
            margin-right: 10px; /* Optional: add spacing between items */
        }
    </style>
</div>