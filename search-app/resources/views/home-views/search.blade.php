<div id="search-methods-radio"> 
    <h3>Search Method</h3>
    <label>
      <input type="radio" v-model="methodSearch" value="keywords" name="search-method"> Keywords
    </label>
    <label>
      <input type="radio" v-model="methodSearch" value="phrase" name="search-method"> Phrase
    </label>
    <label>
      <input type="radio" v-model="methodSearch" value="regularex" name="search-method"> Regular Expression
    </label>
    <label>
      <input type="radio" v-model="methodSearch" value="word-start" name="search-method"> Word Start
    </label>
    <label>
      <input type="radio" v-model="methodSearch" value="word-middle" name="search-method"> Word Middle
    </label>
    <label>
      <input type="radio" v-model="methodSearch" value="word-end" name="search-method"> Word End
    </label>
</div>    

<h3>Languages</h3>
<select v-model="language">
    <option value="latin">Latin</option>
    <option value="scots">Middle Scots</option>
    <option value="dutch">Dutch</option>
</select>

<h3>Spelling Variants</h3>
<select v-model="variant">
    <option value="zero">0</option>
    <option value="one">1</option>
    <option value="two">2</option>
    <option value="three">3</option>
    <option value="four">4</option>
</select>

<div id="volume-select">
    <h3>Please select the volumes you wish to search within</h3>
    <label>
       <input type="checkbox" v-model="volumes" id="volume-1" name="volume1" value="1"> 1
    </label>
    <label>
       <input type="checkbox" v-model="volumes" id="volume-2" name="volume2" value="2"> 2
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

<h3>Page Search</h3>
<input type="search" v-model="pageSearch" id
