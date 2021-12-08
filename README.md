<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">Bitcoin Market Analyser</h3>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#How To Use">How To Use</a>
      <ul>
        <li><a href="#Dependencies">Dependencies</a></li>
        <li><a href="#btcAnalysCLI">btcAnalysCLI</a></li>
        <li><a href="#btcAnalys">btcAnalys</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project utilises the coingecko API to analyse the bitcoin market history. The API can be found at [coingecko](https://www.coingecko.com/en/api).

At the moment the program is able to analyse a given time range of bitcoin data. From the data the program is able to find the longest downward price streak, highest trading volume and the dates to make the best possible profit.

There are plenty of features that could be implemented to this program if so desired.

All the best\
-Daniel


### Built With

* [Python](https://www.python.org/)


<!-- HOW TO USE -->

## How To Use
Start by cloning the repository to your device by
```
git clone https://github.com/dyyyni/bitcoinAnalyser.git
```
Or download the zipfile containing the repository.
For the user, the only files you should be concerned are the btcAnalysCLI.py and the btcAnalys.py which are explained in more detail later on.

### Dependencies
This project utilises the 'Requests' library for the api connection. The library can be installed by running this command
```
python -m pip install requests
```

### btcAnalysCLI
This is a command line interface intented for continuous usage. Start the CLI by running the command inside the directory that contains the project files
```
python btcAnalysCLI.py 
```
To use the program follow the instructions from the command line interface.
Type 'help' for list of commands.

Example:
```
Enter command: setRange
Enter the first date in form (dd/mm/yyyy): 12 8 2020
Enter the last date in form (dd/mm/yyyy): 16 9 2021
Enter command: getData
Enter command: bestProf
The best date to buy is 06/09/2020
The best date to sell is 14/04/2021
```
N.B. Remember to use the command 'getData' after you have set the date range!

### btcAnalys
Sipmplified version intented for backend use.
Run this command in the directory where the project files are located
```
python btcAnalysCLI.py 
```
You will be greeted by the instructions for use:
```btcAnalys.py dd/mm/yyyy dd/mm/yyyy -flag. (-h for options)```
By running
```
python btcAnalysCLI.py -h
```
You will get the flags that can be used by the program.
```-h: help, -dt: longest down trend, -hv: highest trade volume, -bp: best profit```

Example:
```
python btcAnalys.py 12-8-2020 16-9-2021 -bp
06/09/2020 14/04/2021
```

Succesfull usage returns are stripped from extra content to better faciliate the backend use.

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Daniel Luoma - [@danyluoma](https://twitter.com/danyluoma) - daniel.luoma@tuni.fi

Project Link: [https://github.com/dyyyni/bitcoinAnalyser](https://github.com/dyyyni/bitcoinAnalyser)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/github/license/dyyyni/bitcoinAnalyser.svg?style=for-the-badge
[license-url]: https://github.com/dyyyni/bitcoinAnalyser/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/luomadaniel