<!-- resources/views/xquery.blade.php -->

@extends('layouts.app')
@section('title', 'Xquery Page')
@section('content')
<!-- how on earth does it need so many <br>s :0 -->
<br><br><br><br><br><br><br><br><br><br><br><br><br>
<header>
    <div class="header-content">
        <h1 id="xq-title">XQuery Search</h1>
        <p>Some text explaining xquery</p>
    </div>
</header>
<main>
    <div id="xq-info">
        <!-- idealy should display to left of the results -->
    </div>
    <div class="search-section">
        <input 
            type="search"
            placeholder="Enter your query"
            id="xq-box"
        />
        <button id="xq-button">Run</button>   
    </div>
    <div class="results-section">
        <h2 class="results-title">Results</h2>
        <!-- xquery results go here -->
        <code id="xq-results">
            <!--include the output-->
        </code>
    </div>
</main>

@endsection