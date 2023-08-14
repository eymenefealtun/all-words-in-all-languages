# all-words-in-all-languages

<p align="center">
  <img src="https://github.com/eymenefealtun/all-words-in-all-languages/blob/main/mainBanner.png?raw=true" alt="Sublime's custom image"/>
</p>
<p align="center">
         <a href="#backers" alt="Backers on Open Collective">
        <img src="https://img.shields.io/github/commit-activity/t/eymenefealtun/all-words-in-all-languages?style=plastic" /></a>
        <a href="#backers" alt="Backers on Open Collective">
        <img src="https://img.shields.io/github/languages/code-size/eymenefealtun/all-words-in-all-languages?style=plastic" /></a>
                <a href="#backers" alt="Backers on Open Collective">
        <img src="https://img.shields.io/github/stars/eymenefealtun/all-words-in-all-languages?style=plastic" /></a>
                <a href="#backers" alt="Backers on Open Collective">
        <img src="https://img.shields.io/github/watchers/eymenefealtun/all-words-in-all-languages?style=plastic" /></a>
                <a href="#backers" alt="Backers on Open Collective">
        <img src="https://img.shields.io/github/forks/eymenefealtun/all-words-in-all-languages?style=plastic" /></a>
</p>

This repository contains all the words from every language that exists in the universe. Each word is separated by commas, allowing effortless integration into your project as a string array using basic comma-based splitting. If you're seeking an example of how to use it within a project, the [Typing Speed application](https://github.com/eymenefealtun/TarotTyping) utilizes these resources.
  ## How to use?
### [C#](https://learn.microsoft.com/en-us/dotnet/csharp/)
  * Import the txt file into your project.
  * Change its 'Build Action' to Embedded resource and its 'Copy to Output Directory' to Copy if newer from its properties.
  * Assign to a string array;
```plaintext
string[] words= File.ReadAllText(Path.Combine(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location), @"yourFileName")).Split(',');
```

## Created By: [@eymenefealtun](https://github.com/eymenefealtun)
* Linkedin: [@eymenefealtun](https://www.linkedin.com/in/eymen-efe-altun-a1681821b)
* Fiverr: [eymenefealtun](https://www.fiverr.com/eymenefealtun?public_mode=true)
* Youtube: [eymenefealtunn](https://www.youtube.com/@eymenefealtunn/videos)
* Medium: [eymenefealtun](https://medium.com/@eymenefealtun18) 
* Buy me a coffee: [eymenefealtun](https://www.buymeacoffee.com/altuneymenefe) 

## How to contribute?
 1. [Fork](https://github.com/eymenefealtun/all-words-in-all-languages/fork) the repository.
 2. Add new words to the array or introduce languages that haven't been covered yet.
 3. Submit a pull request.
