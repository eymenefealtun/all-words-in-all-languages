# all-words-in-all-languages

<p align="center">
  <img src="https://github.com/eymenefealtun/all-words-in-all-languages/blob/main/mainBanner.png?raw=true" alt="Sublime's custom image"/>
</p>
<p align="center">
         <a href="#backers" alt="Backers on Open Collective">
        <img src="https://img.shields.io/github/commit-activity/t/eymenefealtun/all-words-in-all-languages?style=plastic" /></a>
        <a href="#backers" alt="Backers on Open Collective">
       <img src="https://img.shields.io/github/repo-size/eymenefealtun/all-words-in-all-languages?style=plastic" /></a>
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

### [C++](https://cplusplus.com/doc/tutorial/)

```cpp
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
using namespace std;
int main() {
    ifstream file("yourFileName.txt");
    if (!file) { cerr << "file opening error!" << endl; return 1; }
    string line, word;
    getline(file, line);
    file.close();
    vector<string> words;
    istringstream ss(line);
    while (getline(ss, word, ',')) words.push_back(word);
    for (const string& w : words) cout << w << endl;
    return 0;
}

```
## Available Languages (11)

| Language Name      | Language Native Name | Number of Words         | Word File               |
| ------------------ | -------------------- | ----------------------- | ----------------------- |
| Arabic             | اللغة العربية            |                   5.691.498 |[Words](https://github.com/eymenefealtun/all-words-in-all-languages/blob/main/Arabic/Arabic-5.691.498.txt)  |
| Armenian             |   Հայերէն         |                 981  |[Words](https://github.com/eymenefealtun/all-words-in-all-languages/blob/main/Armenian/Armenian-981.txt)  |
| Azerbaijani        | Azərbaycan dili        |        38.503             |[Words](https://github.com/eymenefealtun/all-words-in-all-languages/blob/main/Azerbaijani/Azerbaijani-38.503.txt)  |
| English            | English              |   466.553              |[Words](https://github.com/eymenefealtun/all-words-in-all-languages/blob/main/English/English-466.553.txt)  |
| French             | Français               |      336.528                 |[Words](https://github.com/eymenefealtun/all-words-in-all-languages/blob/main/French/French-336.528.txt)  |
| Georgian             | ქართული               |      193.210                 |[Words](https://github.com/eymenefealtun/all-words-in-all-languages/blob/main/Georgian/Georgian-193.210.txt)  |
| Greek             | ελληνικά               |      35.279               |[Words](https://github.com/eymenefealtun/all-words-in-all-languages/blob/main/Greek/Greek-35.279.txt)  |
| Kurdish            | Kurdî               |      959                  |[Words](https://github.com/eymenefealtun/all-words-in-all-languages/blob/main/Kurdish/Kurdish-959.txt)  |
| Persian            | فارسی               |      900.357                 |[Words](https://github.com/eymenefealtun/all-words-in-all-languages/blob/main/Persian/Persian-900.357.txt)  |
| Spanish            | Español               |      636.598                 |[Words](https://github.com/eymenefealtun/all-words-in-all-languages/blob/main/Spanish/Spanish-636.598.txt)  |
| Turkish            | Türkçe               |      60.451                   |[Words](https://github.com/eymenefealtun/all-words-in-all-languages/blob/main/Turkish/Turkish-60.451.txt)  |

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

## Sources
* https://github.com/words/an-array-of-spanish-words
* https://github.com/lorenbrichter/Words
* https://github.com/shahind/Persian-Words-Database
* https://www.kaggle.com/datasets/slyce20/aze-words-corpus
* https://psychology.nottingham.ac.uk/greeklex/greeklex1.html
* https://github.com/dwyl/english-words/blob/master/words.txt
* https://github.com/akalongman/geo-words/blob/master/dictionary/txt/ka_GE.txt
