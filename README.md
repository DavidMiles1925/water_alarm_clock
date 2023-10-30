

# Water Alarm Clock

## Table of Contents  
**- [Project Description](#project-description-1)**  
    &emsp;- [About the Product](#about-the-product)  
    &emsp;- [Inspiration](#inspiration)  
    &emsp;- [Project Showcase](#project-showcase)  
    &emsp;&emsp; [Video Overview](#video-overview)

**- [Project Credits](#project-credits)**  
    &emsp;- [Jonathan Hoffman](#jonathan-hoffman---product-owner)  
    &emsp;- [Tom Ryan](#tom-ryan---consulting-engineer)  
    &emsp;- [David Miles](#david-miles---software-developer)  

**- [Documentation](#documentation-1)**  
    &emsp;- [Using Water Alarm](#using-water-alarm)  
    &emsp;- [Technical Notes](#technical-notes)  
    &emsp;- [Hardware](#hardware)  
    &emsp;- [Design](#design)  
    &emsp;- [Software](#software)  
    &emsp;&emsp;- [Dependencies](#dependencies)  
    &emsp;&emsp;- [Current Version](#current-version-07)  
    &emsp;&emsp;- [Future Versions](#future-versions)  
    &emsp;&emsp;- [Previous Versions](#previous-versions)  

---

## Project Description

### About the Product

This is a project in development to create an alarm clock that will spray you with water to help heavy sleepers get out of bed in the morning.

---

### Inspiration

This idea was conceived by Jonathan Hoffman, who has always thought outside of the box. He is a heavy sleeper, and wants something to get him moving quickly in the moring.

---

### Project Showcase
Contents: 
[Video Overview](#video-overview) - 
[Product Image](#product-image) - 
[Design](#design)

#### Video Overview
    -Click here to see a video about the project in it's current state:  

**[Video Overview](https://photos.app.goo.gl/3kBqhnxbUV3KdRak7)**

#### Product Image
    - The alarm clock as of version 0.5:  

<img src="./media/version_0.5_set_up.jpg" width="300" alt="v0.5">

#### Debug Console
    - The debug interface as of version 0.6:  

<img src="./media/v0.6_debug_interface.png" width="300" alt="debug v0.6">

>This interface was used to:
>>**Test individual components of the project.** For example, when testing the buttons I would print a message to the screen when each button was depressed.
>
>>**Display the values of important variables.** When debugging, it was invaluable to know how my variables were set.
>
>>**Display the expected LCD output.** I sent the same string to the console as to the LCD. As I was getting the screen working, this was helpful because I knew if I didn't get the correct output, it was probably an error in my wiring. 
>

---

## Project Credits

### Jonathan Hoffman - Product Owner
>Jonathan, or "Jono" as his friends call him, is the one who initiated this project. He is largely responsible for the mechanical design, and has selected pump and circuit equipment to be used in product construction.

### Tom Ryan - Consulting Engineer
>Tom has been an instrumental part of product testing, solution design, and general consulting. 

### David Miles - Software Developer
>David is responsible for the software and small electronics portion of the project. He is also the one maintaining the project documentation.

---

## Documentation:
Contents: 
[Using Water Alarm](#using-water-alarm) - 
[Hardware](#hardware) - 
[Design](#design) - 
[Software](#software)  

---

### Using Water Alarm:

#### Setting the Alarm  
>>1. Turn the alarm on by pressing the ON/OFF button. The screen should display "ALARM:ON"  
>  
>>2. Hold down the 'SET ALARM' button. The alarm time should appear on the screen.  
>  
>>3. With the 'SET ALARM' button depressed, press the 'HOUR' and 'MINUTE' buttons to set the alarm time.  
>  
>>4. Release the set alarm button. You can check the alarm time at any time by pressing the 'SET ALARM. button.  
>

#### Priming the Pump
>>1. Fill pump reservoir.
>  
>>2. Ensure you have something to catch the water ejected during priming.
>  
>>3. Press 'HOUR' AND 'MINUTE' buttons at the same time. Pump will run for 1 second.
>  

---

### Technical Notes

Contents: [Installation (Raspberry Pi 4)](#install-on-raspberry-pi-4) - 
[Configure to Run on Startup](#configure-to-run-on-startup)

>#### Install on Raspberry Pi 4:
>>1. Configure git:
>>&emsp;a. Install git: [Click Here To Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
>>&emsp;b. Configure:  
>>```bash
>>git config --global user.name "yourusername"
>>git config --global user.email "your@email"
>>```  
>>&emsp;c. Create GitHub Access Token: [Instructions here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic)  
>>&emsp;**SAVE THIS KEY IMMEDIATELY! YOU WILL NOT BE ABLE TO ACCESS IT AGAIN.**  
>  
>>2. Clone repo:
>>&emsp;a. In the terminal, navigate to your desired directory and enter this command:  
>>```bash
>>git clone https://github.com/DavidMiles1925/water_alarm_clock.git  
>>```
>>&emsp;b. You will be prompted for username and key (it is labeled password).  
>>&emsp;**Copy and paste the key generated in step 1c as the password.**  
>  
>>3. Run program:
>>&emsp;a. Run program in console:  
>>```bash
>>cd path/to/program
>>python main.py
>>```
>>&emsp;b. [Configure for startup](#configure-to-run-on-startup)
>  

>#### Configure to Run ON Startup:
>>1. Modify etc/rc.local with admin priviliges:
>>```bash
>>cd /etc
>>sudo nano rc.local
>>```
>>
>>1. Added this line to /etc/rc.local:  
>>```bash  
>>sudo python /home/pi/water_alarm_clock/main.py &  
>>```  
>  
>>2. To stop process, first find pid:  
>>```bash  
>>ps aux | grep "main.py"  
>>```  
>  
>>3. Note the number in the second column.  
>  
>>4. Terminate process:  
>>```bash
>>sudo kill -TERM ###  
>>```  
>>&emsp;*replace "###" with the number from step 3

---

### Hardware:

>Pump info needed  
>Converter info needed  
>Raspberry Pi 4 (Pico in future versions)  
>[1602 LCD Screen](https://lastminuteengineers.com/arduino-1602-character-lcd-tutorial/)  
>[B10K Ohm Potentiometer](https://components101.com/resistors/potentiometer)  
>[5V SL-C Relay](https://www.datasheetcafe.com/srd-05vdc-sl-c-datasheet-pdf/)  
>[4-pin buttons x4](https://components101.com/switches/push-button)  
>Jumper Wires (many assorted m-f, f-f, m-m)  
>220 Ohm Resistor  
>10K Ohm Resistors x4
>LED  

---

### Design

<img src="./media/QPASS_Screenshot.png" width="600" alt="setup diagram">

---

### Software:

#### Dependencies:

>**- Python**  
>Python is natively installed on the Raspberry Pi Pico that will be used in Version 1.0. However, python can be downloaded and installed here: [Install Python](https://www.python.org/downloads/)

---

>#### Current Version: 0.7  
>&emsp;- added snooze feature  
>&emsp;- add set time logic  
>&emsp;- add set time button  
>&emsp;- tweaked snooze output
>&emsp;- adjusted lcd performance
>&emsp;- README:  
>&emsp;&emsp;- add overview video  
>&emsp;&emsp;- add technical notes section  

---

#### Future Versions:

##### Version 0.8
&emsp;- Port to Raspberry Pi Pico:  
&emsp;- Remove console outputs  
&emsp;- Remove OS specific components  
&emsp;- add "no internet" mode  
&emsp;&emsp;- create set_current_time() function  
&emsp;&emsp;- set configuration variable  
&emsp;- Project tuning  

>**Notes on porting to Pico:**  
>   - Need to test with MicroPython  
>   - Need to write code for setting clock  
>               **OR**  
>   - Need to find a way to ping for internet  

Port plan created during version iteration 0.6:

<img src="./media/portplan.png" width="400" alt="v0.6 port plan">

##### Version 1.0   
**This will be the full realease of software, designed to run on the final product.**
##### Version 0.8
&emsp;- Port to Raspberry Pi Pico:  
&emsp;- Remove console outputs  
&emsp;- Remove OS specific components  
&emsp;- add "no internet" mode  
&emsp;&emsp;- create set_current_time() function  
&emsp;&emsp;- set configuration variable  
&emsp;- Project tuning  

>**Notes on porting to Pico:**  
>   - Need to test with MicroPython  
>   - Need to write code for setting clock  
>               **OR**  
>   - Need to find a way to ping for internet  

Port plan created during version iteration 0.6:

<img src="./media/portplan.png" width="400" alt="v0.6 port plan">

##### Version 1.0   
**This will be the full realease of software, designed to run on the final product.**

---

#### Previous Versions:

<details>
    <summary>Previous versions</summary>

##### Version 0.6  
&emsp;- configured to run on startup  
&emsp;- Minor improvements:  
&emsp;&emsp;- optimized sleep times  
&emsp;&emsp;- added exit message on lcd  
&emsp;&emsp;-re-introduced debugging for porting  
&emsp;- Reformated board layout for efficiency  
&emsp;- README:  
&emsp;&emsp;- Project recap  
&emsp;&emsp;- Videos/images  
&emsp;&emsp;- add hardware links  
&emsp;&emsp;- add screen wiring diagram  

##### Version 0.5  
&emsp;- added AM/PM logic  
&emsp;- formated output for AM/PM  
&emsp;- integrated screen  
&emsp;- calibrated potentiometer  
&emsp;- generated screen output to match debug output  
&emsp;- reformatted code for easier reading

##### Version 0.4  
&emsp;- Created basic alarm logic  
&emsp;- integrated indicator LED  
&emsp;- integrated relay circuit  
&emsp;- test all components  

##### Version 0.3  
&emsp;- Set up GPIO pins  
&emsp;- integrated buttons:  
&emsp;&emsp;- alarm on/off  
&emsp;&emsp;- set alarm  
&emsp;&emsp;- hour  
&emsp;&emsp;- minute  
&emsp;- configured button logic  
&emsp;- console debug formatting adjustments  
&emsp;- README:  
&emsp;&emsp;- added table of contents  

##### Version 0.2  
&emsp;- adjusted time output formatting  
&emsp;- created debug output to console  
&emsp;- README update:  
&emsp;&emsp;- hardware  
&emsp;&emsp;- future versioning  

##### Version 0.1  
&emsp;- Created main function  
&emsp;- Created basic utilities library  
&emsp;- Created configuration file  
&emsp;- Initialized repository  
&emsp;- Incorporated bare-bones error handling  
&emsp;- Started README  

</details>

---