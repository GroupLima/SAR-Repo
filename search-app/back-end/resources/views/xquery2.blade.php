@extends('layouts.app')
@section('title', 'XQuery Search')
@section('content')

<div class="container">
<script>
    console.log("HTML content loaded successfully");
</script>
    <header>
        <br><br><br><br><br><br><br><br><br><br><br><br>
        <div class="header-content">
            <h1 id="xq-title">XQuery Search</h1>
            <p>Search through XML documents using XQuery</p>
        </div>
    </header>
    console.log("Vue is initializing...");

    <main id="app">
        <search-xquery></search-xquery>
    </main>
</div>
@endsection

@section('scripts')
<script src="https://cdn.jsdelivr.net/npm/vue@3/dist/vue.global.js"></script>
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
<script src="{{ mix('resources/js/app.js') }}"></script> <!-- Your compiled JS -->
@endsection