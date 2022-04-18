Senior_Project_Code for Wildlife Tracking
Developers: Ernie Lozano, Kevin Nguyen

This step process is how to upload the following code onto the Raspberry Pi Pico.
This code is using Micropython Version 1.18 and Python 3.10

Locate the u2f file for Micropython called "u2f File Micropython". Follow the instructions
    1. Before pulling in the Micro-USB to the Pico or USB to desktop, hold down the boot button. 
        This should open folder explorer, and you should see the Raspberry Pi Pico drive. 
    2. Drag and Drop the u2f file in that drive.
        (You should not be able to see that drive available any more within File Explorer)

Starting up Pycharm GitHub style:
    1. Go to get from VCS
    2. Copy the URL by within the "PipPipDoodlyDoo/Senior_Project_Code" GitHub page, there is a green "Code" button
        Select that and under "HTTPS" copy the URL and insert that to the URL section.
    3. Choose where you want that Repository to be added to your local drive.
    4. If Pycharm did not Pull the latest code, use the Pull function on Pycharm.

On the bottom right of Pycharm you should see:
    UTF-8
    Python 3.10

Set/check if the project implemented Micropython:
    1. Goto Files -> Settings
    2. Goto "Languages & Frameworks"
    3. Select "MicroPython"
    4. Check "Enable MicroPython Support"
    5. Set "Device type: " to "Raspberry Pi Pico"
    6. Check "Auto-detect device path"
        (This should pop up a window that says "Packages required for Raspberry Pi Pico support not found. . .")
        (After uploading the u2f file into the Raspberry Pi, you should be able to Flash without knowing which COM Port is needed)
    7. Select "Missing required MicroPython packages
        (This should download all the libraries that will be used for this project such as Pin and ADC)

Disable Unwanted Folders:
    1. Goto File -> Settings
    2. Goto "Project:Senior_Project_Code"
    3. Select "Project Structure"
    4. If not done yet, highlight every folder EXCEPT ".idea" and mark as "Excluded"
        (This ensures that not all the directories and files get uploaded at once)

Running the Code:
    1. If you want to run the code, open up "Pip_code" to show all the .py files.
    2. Highlight all the .py files and copy or <Ctrl+c>
    3. Right-click the overall folder "Senior_Project_Code" and select "Paste"
    4. Right-click the overall folder again and select "Run 'Flash Senior_Project_Code'"

(The reason for the complication is that I don't believe that you can flash a whole directory. The compiler needs
the code to come from the mail overall folder which is "Senior_Project_Code", and needs to have a main.py. The compiler
searches for that file and runs it. Without that file, it will result to rejecting the code and running the previous Flashed
code. This reiterates the reason why we exclude the directories because it would Flash those Folders into the Pico as well.)

You can use the local terminal to see print functions as well
    1. Under "Tools" -> "MicroPython" -> Select "MicroPython REPL"
        (REPL: Read-evaluation-print loop)
    (If you want to Flash an updated/a new code then you would have to manually exit the terminal by clicking the 'x')