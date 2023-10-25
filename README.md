# Water Alarm Clock

## Table of Contents
**- [Project Description](#project-description-1)**  
**- [Documentation](#documentation-1)**  
    -- [Hardware](#hardware)  
    -- [Software](#software)  
**- [Project Credits](#project-credits)**  

## Project Description

### About the Product

This is a project in development to create an alarm clock that will spray you with water to help heavy sleepers get out of bed in the morning.

### Inspiration

This idea was conceived by Jonathan Hoffman, who has always thought outside of the box. He is a heavy sleeper, and wants something to get him moving quickly in the moring.

## Documentation:

### Hardware:

Raspberry Pi 4 (Pico in future versions)  
Screen  
1-10K Ohm Potentiometer  
5V SL-C Relay  
Buttons x3  
Jumper Wires (many assorted m-f, f-f, m-m)  
220 Ohm Resistor  
10K Ohm Resistors x3  

### Software:

In this section:  
    - [Dependencies](#dependencies)  
    - [Current Version](#current-version-03)  
    - [Previous Versions](#previous-versions)  
    - [Future Versions](#future-versions)  

#### Dependencies:

**- Python**  
Python is natively installed on the Raspberry Pi Pico that will be used in Version 1.0. However, python can be downloaded and installed here: [Install Python](https://www.python.org/downloads/)

#### Current Version: 0.3
    - Set up GPIO pins  
    - Create basic alarm logic  
    - console debug formatting adjustments  
    - README:  
        - add hardware links  
        - add table of contents

#### Previous Versions: 

**Version 0.2**
    - adjusted time output formatting  
    - created debug output to console  
    - README update:  
        - hardware  
        - future versioning  

**Version 0.1**
    - Created main function  
    - Created basic utilities library  
    - Created configuration file  
    - Initialized repository  
    - Incorporated bare-bones error handling  
    - Started README  

#### Future Versions:

**Version 0.4**  
    - integrate "alarm on/off" button  
    - integrate "set alarm" button  
    - integrate "hour" button  
    - integrate "minute" button  
    - configure button logic  

**Version 0.5**  
    - integrate indicator LED  
    - integrate relay circuit  

**Version 0.6**  
    - integrate screen  
    - calibrate potentiometer  
    - generate screen output to match debug output  
    - README:  
        - add screen wiring diagram

**Version 0.7**  
    - configure to start on run  
    - Port to Raspberry Pi Pico  

**Version 1.0**  
    **This will be the full realease of software, designed to run on the final product.**

## Project Credits

### Jonathan Hoffman - Product Owner
Jonathan, or "Jono" as his friends call him, is the one who initiated this project. He is largely responsible for the mechanical design, and has selected pump and circuit equipment to be used in product construction.

### Tom Ryan - Consulting Engineer
Tom has been an instrumental part of product testing, market research, and general consulting. 

### David Miles - Software Developer
David is responsible for the software and small electronics portion of the project. He is also the one maintaining the project documentation.