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
Capacity & scalability
The database contains 5MB of transcribed XML files. It is considered a medium sized database and not expected to increase. However, if the search tool has an increase in the number of users, the website should still be able to handle the influx of activity, especially by following good programming practices that optimize efficiency in every aspect.
The method to access and manage the pictures of the original documents is currently unknown, so we still have to discuss this matter with the client.

Compatibility
Website will be designed for desktop and mobile versions, and should be able to run on any operating system that has an internet browser. Internet Explorer, Chrome, and Firefox may work the best in terms of highlighting search terms within search results.

Security, Reliability & Availability
All pages of the website should be available all the time. 24 hours a day, 7 days a week. In the event of critical failure, the user should be redirected to an appropriate error page. There should also always be a convenient way of contacting the university development team in case part(s) of the website are not working correctly.
The web application will comply with the latest OWASP Top 10 security awareness document. This will keep packages up to date and prevent injections to the database from unauthorized users. These security measures will also include but are not limited to using stored procedures, parameterisation, validating user inputs, and HTTPS.
To check that security measures are consistent and reliable in practice and not just in theory, we will constantly run numerous tests throughout the development process using a suitable testing framework.

Performance, Maintainability & manageability
The University of Aberdeen currently develops their internal systems with the Laravel PHP framework, which is a server side scripting language. As such, this web application will also be developed mainly in the Laravel PHP framework. This will enable the University of Aberdeen software team to support and maintain the product for the future. Additionally, some functionality will be written in JavaScript using Vue framework, a client side scripting language. This will allow some functionality to be run directly on the user’s local machine without needing to wait for the university’s server to receive, process, and respond to the user request. In effect, this will reduce latency and ensure that web interactions feel instantaneous to the user.
Source code will be uploaded to a github repository and managed by the university of aberdeen at the end of this project.

Usability & accessibility
The website should be developed to fit WCAG 2.2 standard. This is a set of criteria which will help content to be more accessible to people with a range of disabilities such as blindness, hearing impairments, speech disabilities, photosensitivity, and cognitive limitations. Tools such as WAVE, Axe, and chrome dev tools can be used to validate compliance in different browsers.
The user experience should be efficient and satisfying. The purpose of each interaction should be clear and easily understood to the user, and there should be a logical followup response to any user action. Our team will design the website centered around the user’s needs because navigating the website should be simple, intuitive, and overall as user friendly as possible. 
Furthermore, we aim to achieve a simple but aesthetic layout to maximize user enjoyment and satisfaction. The UI should be designed in a way that is professional, learnable, and cohesive for people that have a range of disabilities.

Programming and scripting languages
Front end
The website will be constructed with HTML
CSS styling will be done using SAAS framework
Functionality between the server and the client (user) will be written in PHP using Laravel Framework
Local functions will be written in Javascript using Vue Framework
Backend
Python will be used for querying data in the database
Testing
To perform all of our tests, we will use PHPUnit testing framework
___

### PROJECT TIMING (andy)

___

### DEFINITIONS AND ACRONYMS (piotr & dermot)

___
