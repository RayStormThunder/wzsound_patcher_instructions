# WZSound Patcher Instruction Generator

The WZSound Patcher Instruction program is a program design to make the modification of .brsar files, more specifically WZSound.brsar, much easier to do.
This program is intended to be useful for SSRando by making the patching of the file easier and faster. 
This program can be used to patch WZSound files for both SD and HD (If you have both WZSound files from their respective games.)
It also creates a patch instruction folder for SD which creates a folder of all the rwav files you want to modify along with a file explaining where those rwavs should be patched.


# The following is the steps of how the program operates:

1. Create a Project.
    a. A project folder can be created by either creating a new project or converting a previously modified WZSound.
    b. Creating a new project just creates a folder with the name you give it, to store all future changes.
    c. Converting a project will ask for a modified WZSound. It will then convert that file into a project.
    d. You can load any of your projects.

2. Select instruction files to get the sounds you want to edit.
    a. An instruction file is a YAML containing information on which RWAVs from which indexes need to be extracted.
    b. The user can edit or create new instruction files if they wish, or can use the default ones.
        1. The program itself has the ability to create and edit YAMLs.
        2. When you give the WZSound, it will create an "Index" folder which will contain all indexes from WZSound.
        3. You can use the information in that folder to create new instructions.
    c. Instruction files can be created and shared with others.

3. Create a project BRWSD.
    a. A project BRWSD file is a BRWSD file with every RWAV file you want to modify in it.
    b. BRWSD can be modified by BrawlCrate and saved (unlike .brsar files), which makes working on it easy.

4. Create the Patcher Instructions.
    a. This creates a folder with the RWAV files you modified from the BRWSD project.
    b. It also has an instruction file that says where one of those RWAV files needs to be patched in WZSound.

5. Patch to SD WZSound.
    a. The sounds get patched by inserting the RWAV data at the location specified by the instruction file created in the last step.

6. Patch to HD WZSound.
    a. This will basically just search for the unmodified RWAVs, and when found in the HD WZSound, will insert the modified RWAV at that location.
