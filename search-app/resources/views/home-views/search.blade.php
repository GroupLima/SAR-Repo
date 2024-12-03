<!-- resources/views/search.blade.php -->
<!-- put search components here -->

<!-- SASS people please read!
      I have used ids, rather than classes, to identify each form option, because the purpose of ids is to identify single, unique elements.
      Hopefully its enough so that the search class people can link it all together.
      Classes are for grouping multiple elements together so i used them to identify areas that might have similar styling and behaviour to
      each other. -->

<div id="search-methods-radio" class="advanced-option"> 
   <h3 class="option-title">Search Method</h3>
   <label>
      <input type="radio" v-model="methodSearch" value="keywords" id="keywords" name="search-method"> Keywords
   </label>
   <label>
      <input type="radio" v-model="methodSearch"  value="phrase" id="phrase" name="search-method"> Phrase
   </label>
   <label>
      <input type="radio" v-model="methodSearch" value="regularex" id="regularex" name="search-method"> Regular Expression
   </label>
   <label>
      <input type="radio" v-model="methodSearch" value="starts with" id="word-start" name="search-method"> Word Start
   </label>
   <label>
      <input type="radio" v-model="methodSearch" value="word-middle" id="word-middle" name="search-method"> Word Middle
   </label>
   <label>
      <input type="radio" v-model="methodSearch" value="word-end" id="word-end" name="search-method"> Word End
   </label>
</div>
<div class="advanced-option">    
   <h3 class="option-title">Languages</h3>
   <select v-model="language"id="language">
      <option value = "any">Any</option>
      <option value="latin">Latin</option>
      <option value="scots">Middle Scots</option>
      <option value="dutch">Dutch</option>
   </select>
</div>   
<div class="advanced-option">
   <h3 class="option-title">Spelling Variants</h3>
   <select v-model="variant" id="variant">
      <option value="0">0</option>
      <option value="1">1</option>
      <option value="2">2</option>
      <option value="3">3</option>
      <option value="4">4</option>
   </select>
</div>   
<div id=volume-select class="advanced-option">
   <!-- Maybe a toggle button to automatically select all would be good-->
   <h3 class="option-title">Volume</h3>
      <input type="checkbox" v-model="volumes" id="volume-1" name="volume1" value="1"> 1
   </label>
   <label>
      <input type="checkbox" v-model="volumes"id="volume-2" name="volume2" value="2"> 2
   </label>
   <label>
      <input type="checkbox" v-model="volumes" id="volume-3" name="volume3" value="3"> 3
   </label>
   <label>
      <input type="checkbox" v-model="volumes" id="volume-4" name="volume4" value="4"> 4
   </label>
   <label>
      <input type="checkbox" v-model="volumes" id="volume-5" name="volume5" value="5"> 5
   </label>
   <label>
      <input type="checkbox" v-model="volumes" id="volume-6" name="volume6" value="6"> 6
   </label>
   <label>
      <input type="checkbox" v-model="volumes" id="volume-7" name="volume7" value="7"> 7
   </label>
   <label>
      <input type="checkbox" v-model="volumes" id="volume-8" name="volume8" value="8"> 8
   </label>
</div>
<!-- We need a constraint to restrict between 1 and the max page number -->
<div class="advanced-option">  
   <h3 class="option-title">Page Search</h3> 
   <input type="search" v-model="pageSearch" id="page-search" placeholder="1, 69, 591...">
</div>  
<!-- We need a constraint to restrict between 1 and the number of entries -->
<div class="advanced-option">
   <h3 class="option-title">Entry</h3>
   <input type="search" v-model="entrySearch" id="entry-search" placeholder="1, 2, 3, 4...">
</div>
<!-- We need to apply constraints to limit date between 1398 and 1510 -->
<div id="dates" class="option-title">
   <h3 class="option-title">Date Range</h3>
   <label>
      from <input type="date" v-model="startDate" id="start-date" name="start-date">
   </label>   
   <label>
      to <input type="date" v-model="endDate" id="end-date" name="end-date">
   </label>  
</div>
<!-- We should only allow valid DocIDs -->
<div class="advanced-option">
   <h3 class="option-title">Doc ID</h3>
   <input type="search" v-model="docId" id="doc-id-search" placeholder="ARO-1-0001-01">
</div>



