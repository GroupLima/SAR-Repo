<template>
    <div class="help-page">
        <!-- Main Section -->
        <main class="content">
            <div class="container-help">
                <h1>Help Page</h1>
                <p class="help-intro">Welcome to the help page. Here you can find information about how to use our search, browse, and XQuery features.</p>
                
                <div class="help-section">
                    <button class="help-dropdown-button" @click="toggleSection('search')">
                        Search
                        <span class="dropdown-arrow" :class="{ 'open': openSections.search }">▼</span>
                    </button>
                    <div class="help-dropdown-content" :class="{ 'active': openSections.search }">
                        <div class="help-content">
                            <h3>Basic Search</h3>
                            <p>To perform a simple search:</p>

                            <ul>
                                <li>Enter your search term in the main search box</li>
                                <li>Select your search method from the dropdown (Keywords, Phrase, Regex, Word Start, Word Middle, or Word End)</li>
                                <li>Click the "SEARCH" button or press Enter</li>
                            </ul>

                            <h3>Search Preferences</h3>
                            <p>You can adjust your search preferences:</p>

                            <ul>
                                <ul><b>Search method</b>: Choose how your search term is matched (default is "Word Start")</ul>
                                <ul><b>Variants</b>: Select the level of spelling variants to include (0-4)</ul>
                                <ul><b>Results per page</b>: Choose how many results to display (5, 10, 20, 30, or 50)</ul>
                                <ul><b>Sort by</b>: Select how to order your results (Frequency within result, Volume ascending/descending, or Chronological)</ul>
                            </ul>
                            
                            <h3>Advanced Search</h3>
                            <p>Click "ADVANCED SEARCH ▼" to access additional filters:</p>

                            <ul>
                                <ul><b>Languages</b>: Filter by language (Any, Latin, Middle Scots, or Dutch)</ul>
                                <ul><b>Volume</b>: Select specific volumes to search (1, 2, 4, 5, 6, 7, 8) or choose "All"</ul>
                                <ul><b>Page Search</b>: Find content on specific pages (enter page numbers)</ul>
                                <ul><b>Entry</b>: Search for specific entry numbers</ul>
                                <ul><b>Date Range</b>: Filter results by date (use the date pickers)</ul>
                                <ul><b>Doc ID</b>: Search for a specific document ID (e.g., ARO-1-0001-01)</ul>
                            </ul>

                            <p>Use "Reset Field Values" to clear all advanced search filters.</p>
                            
                        </div>
                    </div>
                </div>
                
                <div class="help-section">
                    <button class="help-dropdown-button" @click="toggleSection('browse')">
                        Browse
                        <span class="dropdown-arrow" :class="{ 'open': openSections.browse }">▼</span>
                    </button>
                    <div class="help-dropdown-content" :class="{ 'active': openSections.browse }">
                        <div class="help-content">
                            <h3>Volume Navigation</h3>
                            <p>Use the volume selector to choose specific volumes to browse through.</p>
                            
                            <h3>Page Navigation</h3>
                            <p>Navigate between pages using the navigation controls. You can jump to a specific page by entering the page number.</p>
                            
                            <h3>Viewing Records</h3>
                            <p>Records associated with each page are displayed in the right panel. Click on a record to see more details.</p>
                            
                            <h3>XML View</h3>
                            <p>Click the "View XML" button to see the XML structure of a record.</p>

                            <h3>Export PDF</h3>
                            <p>Click the "Add to selected" checkbox and navigate to the nes "Selected" tab in the navigation bar to view all selected records.</p>
                            <p>Click the "Export as PDF" button to download a PDF of the selected records, the "Remove" button to clear the corresponding record, or the "Clear All" button to clear all selected records.</p>
                        </div>
                    </div>
                </div>
                
                <div class="help-section">
                    <button class="help-dropdown-button" @click="toggleSection('xquery')">
                        XQuery
                        <span class="dropdown-arrow" :class="{ 'open': openSections.xquery }">▼</span>
                    </button>
                    <div class="help-dropdown-content" :class="{ 'active': openSections.xquery }">
                        <div class="help-content">
                            <h3>Using XQuery</h3>
                            <p>XQuery is a powerful query language for searching XML data. Use it to create complex queries for the ARO database.</p>
                            
                            <h3>XQuery Syntax</h3>
                            <p>Basic XQuery expressions follow this format:</p>
                            <pre>for $x in collection("documents")
where $x/title contains text "keyword"
return $x</pre>
                            
                            <h3>Examples</h3>
                            <p>Here are some example queries you can modify for your needs:</p>
                            <ul>
                                <li>Search by date: <code>where $x/date >= "1800-01-01" and $x/date <= "1900-12-31"</code></li>
                                <li>Search by author: <code>where $x/author = "Smith"</code></li>
                                <li>Combine conditions: <code>where $x/title contains text "history" and $x/language = "english"</code></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script>
export default {
    data() {
        return {
            openSections: {
                search: false,
                browse: false,
                xquery: false
            }
        };
    },
    methods: {
        toggleSection(section) {
            this.openSections[section] = !this.openSections[section];
        }
    }
};
</script>