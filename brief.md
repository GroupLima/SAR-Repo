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

The key demographic of the webpage and search tool will consist of users aged 18 and above with a range of technological skills and experiences. The primary audience includes academic researchers and students with specific interests in the subject material. The secondary audience includes non-specialists who have a general interest in records and transcripts. To ensure that the webpage and search tool are accessible to all, steps will be taken to create a usable and accessible user interface with clear directions and instructions.

The webpage and search tool will be used to search and navigate the Aberdeen registers, a valuable historical resource. The webpage will access the search tool and information about the tool and registers. It will also include external links to the [University of Aberdeen registers page](https://www.abdn.ac.uk/riiss/projects/aberdeen-registers-online-213.php) and the [Aberdeen registers blog page](https://aberdeenregisters.org/blog/).

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
- user experience (ux) relating to ui design 
	- back-end: python

___


### PROJECT TIMING

The development methodology chosen to carry out this project is agile development. Following this, it was concluded that the one week sprints are most appropriate length given both the time-frame and other responsibilities of our coursework. This layout will give us the best environment to optimize our performance. Our sprint planning sessions will be held every Monday at 16:00 P.M. and further into the week, the classic sprint workflow will be kept to. Each iteration will allow us to incrementally progress towards a deliverable product for the client, for which we will have a further three or four sprints for.

___

### DEFINITIONS AND ACRONYMS (piotr & dermot)
- Aberdeen Registers Online: 1398-1511 (ARO) is a digital transcription of the first eight volumes of the Aberdeen Council Registers. [definition from https://www.abdn.ac.uk/aro]
- Law in the Aberdeen Council Registers, 1398-1511: Concepts, Practices, Geographies (LACR) was a project to create a digital textual resource from the registers. This was achieved by creating a transcription and TEI-compliant mark-up of the entire corpus of text from the registers covering 1398-1511. [definition from https://aberdeenregisters.org/project/]
- Search Aberdeen Registers is a prototype web application to facilitate search within the Aberdeen Registers Online (ARO) corpus. [definition from https://sar.abdn.ac.uk]

ARO - Aberdeen Registers Online
<br> LACR - Law in the Aberdeen Council Registers 
<br> SAR - Search Aberdeen Registers
<br> TEI - Text Encoding Initiative (An organisation which has developed guidlines for presenting text online for research, teaching and preservation)
<br> XML - Extensible Markup Language (Used for data representation and storage)
<br> PHP - Hypertext Preprocessor (oginally stands for Personal Home Page) - powerful programming langage that is commonly used when buidling websites
<br> UI - User Interface
<br> UX - User Experience
<br> HTML - Hypertext Markup Language (Used for the front end of a website, basic layout etc)
<br> CSS - Cascading Style Sheets (Used for the front end, to simplify the html, and to make the UX uniform)



___
