# Water Alarm Clock

## Table of Contents  
**- [Project Description](#project-description-1)**  
    &emsp;- [About the Product](#about-the-product)  
    &emsp;- [Inspiration](#inspiration)  
**- [Documentation](#documentation-1)**  
    &emsp;- [Hardware](#hardware)  
    &emsp;- [Software](#software)  
    &emsp;&emsp;- [Dependencies](#dependencies)  
    &emsp;&emsp;- [Current Version](#current-version-05)  
    &emsp;&emsp;- [Future Versions](#future-versions)  
    &emsp;&emsp;- [Previous Versions](#previous-versions)  
**- [Project Credits](#project-credits)**  
    &emsp;- [Jonathan Hoffman](#jonathan-hoffman---product-owner)  
    &emsp;- [Tom Ryan](#tom-ryan---consulting-engineer)  
    &emsp;- [David Miles](#david-miles---software-developer)  

## Project Description

### About the Product

This is a project in development to create an alarm clock that will spray you with water to help heavy sleepers get out of bed in the morning.

### Inspiration

This idea was conceived by Jonathan Hoffman, who has always thought outside of the box. He is a heavy sleeper, and wants something to get him moving quickly in the moring.

## Documentation:

### Hardware:

Pump info needed  
Converter info needed  
Raspberry Pi 4 (Pico in future versions)  
[1602 LCD Screen](https://lastminuteengineers.com/arduino-1602-character-lcd-tutorial/)  
[B10K Ohm Potentiometer](https://components101.com/resistors/potentiometer)  
[5V SL-C Relay](https://www.datasheetcafe.com/srd-05vdc-sl-c-datasheet-pdf/)  
[4-pin buttons x4](https://components101.com/switches/push-button)  
Jumper Wires (many assorted m-f, f-f, m-m)  
220 Ohm Resistor  
10K Ohm Resistors x4
LED  

### Software:

#### Dependencies:

**- Python**  
Python is natively installed on the Raspberry Pi Pico that will be used in Version 1.0. However, python can be downloaded and installed here: [Install Python](https://www.python.org/downloads/)

#### Current Version: 0.6  
    - configure to run on startup  
    - Port to Raspberry Pi Pico  
        &emsp;- Remove console outputs  
        &emsp;- Remove OS specific components  
    - README:  
        &emsp;- Project recap  
        &emsp;- Videos/images  
        &emsp;- add hardware links  
        &emsp;- add screen wiring diagram  

<img src="./media/version_0.5_set_up.jpg" width="400" alt="v0.5">

#### Future Versions:

**Version 0.7**  
    - Project tuning


**Version 1.0**  
    **This will be the full realease of software, designed to run on the final product.**

#### Previous Versions:

**Version 0.5**
    - added AM/PM logic
    - formated output for AM/PM
    - integrated screen  
    - calibrated potentiometer  
    - generated screen output to match debug output  
    - reformatted code for easier reading

**Version 0.4**  
    - Create basic alarm logic  
    - integrate indicator LED  
    - integrate relay circuit  
    - test all components  


**Version 0.3**  
    - Set up GPIO pins  
    - integrate buttons:  
        &emsp;- alarm on/off  
        &emsp;- set alarm  
        &emsp;- hour  
        &emsp;- minute  
    - configure button logic  
    - console debug formatting adjustments  
    - README:  
        &emsp;- add table of contents  

**Version 0.2**  
    - adjusted time output formatting  
    - created debug output to console  
    - README update:  
        &emsp;- hardware  
        &emsp;- future versioning  

**Version 0.1**  
    - Created main function  
    - Created basic utilities library  
    - Created configuration file  
    - Initialized repository  
    - Incorporated bare-bones error handling  
    - Started README  


## Project Credits

### Jonathan Hoffman - Product Owner
Jonathan, or "Jono" as his friends call him, is the one who initiated this project. He is largely responsible for the mechanical design, and has selected pump and circuit equipment to be used in product construction.

### Tom Ryan - Consulting Engineer
Tom has been an instrumental part of product testing, solution design, and general consulting. 

### David Miles - Software Developer
David is responsible for the software and small electronics portion of the project. He is also the one maintaining the project documentation.