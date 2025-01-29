@php
    $vueAssetsPath = public_path('vue/assets');
    $jsFiles = glob($vueAssetsPath . '/*.js');
    $cssFiles = glob($vueAssetsPath . '/*.css');

    $jsFile = count($jsFiles) > 0 ? basename($jsFiles[0]) : '';
    $cssFile = count($cssFiles) > 0 ? basename($cssFiles[0]) : '';
@endphp

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lima SAR</title>
    @vite(['resources/sass/app.scss']) <!-- Include Laravel styles if needed -->

    <!-- Load Vue CSS files dynamically -->
    @foreach($cssFiles as $css)
        <link rel="stylesheet" href="{{ asset('vue/assets/' . basename($css)) }}">
    @endforeach
</head>
<body>
    <div id="app"></div>

    <!-- Load Vue JS files dynamically -->
    @foreach($jsFiles as $js)
        <script type="module" src="{{ asset('vue/assets/' . basename($js)) }}"></script>
    @endforeach
</body>
</html>
