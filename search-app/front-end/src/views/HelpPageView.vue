<template>
    <div class="help-page">
        <!-- Main Section -->
        <main class="content">
            <div class="container-help">
                <h1>Help</h1>
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
                                <li>Click the "SEARCH" button or press Enter to see the entries in the historical records that match your search term</li>
                            </ul>

                            <h3>Search Preferences</h3>
                            <p>You can adjust your search preferences:</p>

                            <ul>
                                <ul><b>Search method</b>: Choose how your search term is matched (default is "Keywords")</ul>
                                <ul><b>Variants</b>: Select the level of spelling variants to include (0 to 40%)</ul>
                                <ul><b>Results per page</b>: Choose how many results to display (5, 10, 20, 30, or 50)</ul>
                                <ul><b>Sort by</b>: Select how to order your results (Best Match, Frequency within result, Volume ascending/descending, or Chronological)</ul>
                            </ul>
                            
                            <h3>Advanced Search</h3>
                            <p>Click "ADVANCED SEARCH ▼" to access additional filters:</p>

                            <ul>
                                <ul><b>Languages</b>: Filter by language (Any, Latin, Middle Scots, Dutch, or Multiple)</ul>
                                <ul><b>Volume</b>: Select specific volumes to search (1, 2, 4, 5, 6, 7, 8) or choose "All" to toggle all check boxes on and off</ul>
                                <ul><b>Page Search</b>: Find content on specific page(s) (enter page numbers, separated by commas)</ul>
                                <ul style="display: None;"><b>Entry</b>: Search for specific entry numbers</ul>
                                <ul><b>Date Range</b>: Filter results by date using the date pickers, selecting a year only, year and month or the full date</ul>
                                <ul><b>Doc ID</b>: Search for a specific document ID or entry (e.g., ARO-1-0001-01)</ul>
                            </ul>

                            <p>You do not need to enter a search term in the bar if you have selected an advanced filter<br>Use "Reset Field Values" to clear all advanced search filters</p>

                            <h3>Search Methods</h3>
                            <p>Determine how your search term text is handled when matching with the entry texts:</p>

                            <ul>
                                <ul><b>Word Start</b>: Look for a string of characters that appears at beginning of words</ul>
                                <ul><b>Word Middle</b>: Look for a string of characters that appears in the middle of words</ul>
                                <ul><b>Word End</b>: Look for a string of characters that appears at end of words</ul>
                                <ul><b>Keywords</b>: Search for individual words in the entries. You can search for multiple words at once, separating them with a space.</ul>
                                <ul><b>Phrase</b>: Search for one or more consecutive words</ul>
                                <ul><b>Regex</b>: Find patterns in the entries using a 'regular expression'. See <a href="https://www.w3schools.com/python/python_regex.asp">here</a> for syntax.</ul>
                            </ul>
                            
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
                            <p>Use the volume selector to choose a volume to browse through.</p>
                            
                            <h3>Page Navigation</h3>
                            <p>Switch between pages using the navigation controls. You can jump to a specific page by entering the page number.</p>
                            
                            <h3>Viewing Records</h3>
                            <p>Records associated with each page are displayed in the right panel. Pictures of the page are on the left.</p>
                            
                            <h3>XML View</h3>
                            <p>Click the "Switch to XML" button to see the XML structure of an entry.</p>

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
                            <p>The XQuery expressions will generally follow this format:</p>
                            <pre>/axis:elementName[@attributeName="value"]</pre>
                            
                            <h3>Examples</h3>
                            <p>Here are some example queries:</p>
                            <ul>
                                <li>Return all records in Latin: 
                                    <br>
                                    <code>//ns:div[@xml:lang="la"]</code></li>
                                    Instead of "la", use "sc" to return Scots text and "mul" for Multiple
                                    <br>
                                    <li>Return records of a specific date:
                                    <br>
                                    <code>//ns:div[.//ns:date[@when="1398-09-30"]]</code></li>
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