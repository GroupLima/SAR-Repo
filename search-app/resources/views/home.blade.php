<!-- resources/views/home.blade.php -->

@extends('layouts.app')
@section('title', 'Home Page')
@section('content')
        <h2>This is the home page</h2>
        <div id = title>
            <h1>SRA 2.0</h1> 
        </div>
        @include('home-views.search')
        <img src="images/university.png" alt="University Logo" class="bottom-image">
@endsection
