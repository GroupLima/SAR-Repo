<!-- resources/views/xquery.blade.php -->

@extends('layouts.app')
@section('title', 'Xquery Page')
@section('content')
<<<<<<< Updated upstream
    <h2>This is the xquery page</h2>
=======
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
            v-model="query"
            id="xq-box"
        />
        <button id="xq-button" @click="runQuery">Run</button>   
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
@section('scripts')
<script src="https://cdn.jsdelivr.net/npm/vue@3/dist/vue.global.js"></script>
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
<script src="{{ asset('compiled-js/home.js') }}"></script>
>>>>>>> Stashed changes
@endsection