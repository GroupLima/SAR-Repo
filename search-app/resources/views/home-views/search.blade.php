<!-- resources/views/search.blade.php -->
<!-- put search components here -->

<div id="search-methods-radio"> 
    <h3>Search Method</h3>
    <label>
      <input type="radio" id="keywords" name="search-method"> Keywords
    </label>
    <label>
      <input type="radio" id="phrase" name="search-method"> Phrase
    </label>
    <label>
      <input type="radio" id="regularex" name="search-method"> Regular Expression
    </label>
    <label>
      <input type="radio" id="word-start" name="search-method"> Word Start
    </label>
    <label>
      <input type="radio" id="word-middle" name="search-method"> Word Middle
    </label>
    <label>
      <input type="radio" id="word-end" name="search-method"> Word End
    </label>
</div>    
<h3>Languages</h3>
<select id="language">
    <option value="latin">Latin</option>
    <option value="scots">Middle Scots</option>
    <option value="dutch">Dutch</option>
</select>
<h3>Spelling Variants</h3>
<select id="varients">
    <option value="zero">0</option>
    <option value="one">1</option>
    <option value="two">2</option>
    <option value="one">3</option>
    <option value="two">4</option>
</select>
<div id=volume-select>
    <h3>Please select the volumes you wish to search within</h3>
    <label>
       <input type="checkbox" id="volume-1" name="volume1" value="1"> 1
    </label>
    <label>
       <input type="checkbox" id="volume-2" name="volume2" value="2"> 2
    </label>
    <label>
       <input type="checkbox" id="volume-3" name="volume3" value="3"> 3
    </label>
    <label>
       <input type="checkbox" id="volume-4" name="volume4" value="4"> 4
    </label>
    <label>
       <input type="checkbox" id="volume-5" name="volume5" value="5"> 5
    </label>
    <label>
       <input type="checkbox" id="volume-6" name="volume6" value="6"> 6
    </label>
    <label>
       <input type="checkbox" id="volume-7" name="volume7" value="7"> 7
    </label>
    <label>
       <input type="checkbox" id="volume-8" name="volume8" value="8"> 8
    </label>
</div>
<h3>Page Search</h3><!-- this needs constraints, so does any search bar -->
<input type="search" id="page-search" placeholder="1, 69, 591...">
<h3>Entry</h3>
<input type="search" id="entry-search" placeholder="1, 2, 3, 4...">
<h3>Date Range</h3><!--we need to apply constraints to the date -->
<div id="dates"> <!-- it truly looks so sad and squished rn, so the empty space needs utilised -->
   <label><!-- for some reason the label and date box display wrong way round -->
      from <input type="date" id="start-date" name="start-date">
   </label>   
   <label>
      to <input type="date" id="end-date" name="end-date">
   </label>  
</div>
<h3>Doc ID</h3>
<input type="search" id="doc-id-search" placeholder="ARO-1-0001-01">