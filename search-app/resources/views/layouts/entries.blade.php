<!-- resources/views/layouts/entries.blade.php -->

<!-- Include Prism.js for syntax highlighting -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.23.0/themes/prism.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.23.0/prism.min.js"></script>

<style>
    .entries-col {
        width: 100%; /* Full width of the container */
    }
</style>

<!-- gets $entries from xml controller -->
<div class="entries-col">
    @foreach ($entries as $entry)
        <div class="panel">
            <div class="metadata">
                Metadata
                <div>id: {!! $entry['id'] !!}</div>
                <div>date: {!! $entry['date'] !!}</div>
                <div>volume: {!! $entry['volume'] !!}</div>
                <div>chapter: {!! $entry['chapter'] !!}</div>
                <div>page: {!! $entry['page'] !!}</div>
                <div>language: {!! $entry['language'] !!}</div>
                <!--
                all entry values you can use:
                    xml
                    inner_text
                    type
                    id
                    volume
                    chapter
                    page
                    date
                    language
                -->
            </div>
            <!-- xml view -->
            <pre class="language-xml">
                <code>
                    <!-- display xml -->
                    {!! $entry['xml'] !!};
                </code>
            </pre>
            <!-- normal text view (toggle between xml and text using hidden class) -->
            <div class="text-view hidden">
                <div class="text">
                    <!-- displayer innerXml -->
                    {!! $entry['inner_text'] !!}
                </div>
            </div>
            
        </div>
    @endforeach
</div>

