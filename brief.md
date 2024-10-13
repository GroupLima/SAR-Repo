**Helpful resource:** [How to write SRS](https://www.perforce.com/blog/alm/how-write-software-requirements-specification-srs-document)
Start with bullet points and we will buff it out into paragraphs after.
___
## BRIEF

### TABLE OF CONTENTS

#### Client Meeting
#### Introduction: Purpose and Objectives
#### Target Audience and Intended Usage
#### Functional Requirements
#### Nonfunctional Requirements
#### Project Timing
#### Definitions and Acronyms

___
### CLIENT MEETING

___
### INTRODUCTION: PURPOSE AND OBJECTIVES (fariha)

This project aims to improve the previous version of Search Aberdeen Registers (SAR) (https://sar.abdn.ac.uk/#homepage), which was created in 2017. We will recreate the search tool using PHP, aligning with current practice and aiding future support and maintenance. The front end of the webpage will be developed using JavaScript and CSS. GitHub will be the source code repository and version control, and PHPUnit will be the testing framework. The target audience is academic researchers and students with a specialist interest in the content. A secondary audience includes those who are curious about the records and transcripts.


- rough summary of general goals and objectives goes here (scope)
	- i.e improve upon 2017 version
	- use php instead of ruby
- who the tool is for (jackson)
- who lima is (project manager, product master, scrum master, other roles?)

___
### TARGET AUDIENCE AND INTENDED USAGE (rebekah)

The primary audience of the webpage and search tool includes academic researchers and students with specific interest in the topic. The secondary audience includes non-specialists who have a general interest in the records and transcripts.

It will be kept in mind that some of these users are novices at technology.

- experts in the field, but may be novice technology users

___
### FUNCTIONAL REQUIREMENTS

Most importantly, our version of the search tool must retain the existing functionality of Search Aberdeen Registers. What this involves, is creating both basic and advanced search functions, and giving the user the ability to browse through each volume, page and entry.

In the advanced search, the user should be able to search for a word, expression or phrase and filter the results in various ways (i.e., page, date, content, language). They should also be able to search at the beginning, middle and end of words for their desired string of characters, and check for spelling variants. The search results should display a list of entries that include the desired expression, with the matches highlighted in the entry. Additionally, the search results should have the option of sorting by volume & page, frequency and chronology, as well as the option of choosing the number of results per page. The document ID, volume, page and date should be shown for every entry.

While browsing or searching, if the user selects a page, the site should display a picture of the page, as well as transcriptions of all the entries on that page, noting the ID, date and language. Hovering over the picture should zoom in on where the cursor is. Lastly, there should be the option to switch to an XML view of the transcription.

The current edition of the tool does not allow for highlighting and copying of the text on a transcription, so this will be added, as well as any additional fuctions as the client wishes (i.e., new searches, quality of life improvements)

Lastly, the user should be able to search through the XML files using XQuery.


___
### NONFUNCTIONAL REQUIREMENTS (caitlin & haziel)
- performance, security, usability, accessibility, reliability and scalability
- programming and scripting languages
	- front-end: php, javascript, css, html
	- back-end: up to us?
- user experience relating to ui design (ux)
	- back-end: python

___

### PROJECT TIMING (andy)

___

### DEFINITIONS AND ACRONYMS (piotr & dermot)

___
