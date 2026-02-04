def get_hover_descriptions() -> dict[str, str]:
	return {
        "button_create_project": """
                <div style='font-size:14pt;'>Create SD Project</div>
                <div>
                        This button will create a new project with a name you give it.
                        This is to be used if you want a completely new project.
                        If you already have a modified WZSound that you edited in the past,
                        try looking at the, '<b>Convert Modified SD WZSound to Project,</b>' instead.
                </div>
                <br>
                <div>
                        After you create a project you will be able to load the project in the
                        future with the, '<b>Load SD Project,</b>' button.
                </div>
                <br>
                <div>
                        Try to name your project something that makes it clear what it is for.
                        For example, if you are making a WZSound where you replaced Link's voice
                        with Mario's voice, you could call it something like: 'Mario Voice Pack.'
                </div>
        """,

        "button_convert_project": """
                <div style='font-size:14pt;'>Convert SD Project</div>
                <div>
                        This button lets you convert a previously modified WZSound into a project folder.
                        Use this if you've already edited a WZSound file in the past and want to bring that work
                        into the patcher system without starting over.
                </div>
                <br>
                <div>
                        This will also create an 'RWAV Instruction' file which is basically a file that says
                        what Index and Audio[#] your sounds were found at. It will the automatically make a
                        BRWSD Project with that information. And unlike '<b>Create SD Project</b>' it will
                        automatically fill the BRWSD Project with sounds you have already replaced.
                </div>
                <br>
                <div>
                        From there you can either add more 'RWAV Instruction' files to your project and replace
                        even more sounds. You could also '<b>Create SD WZSound Patcher Instructions</b>' or
                        you could '<b>Patch HD WZSound.</b>'
                </div>
        """,

        "button_load_project": """
                <div style='font-size:14pt;'>Load SD Project</div>
                <div>
                        Use this button to open an existing project you previously created or converted.
                        Once loaded, you can: <br>
                        '<b>Create, Edit, Move, RWAV Extraction Instructions</b>',<br>
                        '<b>Create SD WZSound Patcher Instructions</b>',<br>
                        '<b>Patch SD WZSound</b>',<br>
                        '<b>Patch HD WZSound</b>',
                </div>
                <br>
                <div>
                        In the case you have multiple projects. You will load your project by selecting it
                        via a dropdown. The dropdown will be sorted by, 'last modified.'
                </div>
        """,

        "list_options": """
                <div style='font-size:14pt;'>Excluded RWAV Instructions</div>
                <div>
                        This list contains a bunch of instruction files. These instruction files
                        explain what RWAVs to extract from what indexes. They are given names to
                        represent what types of sounds they will extract. For example, 'Link Sound Effects,'
                        will extract all of Link's sound effects into your project BRWSD if included.
                </div>
                <br>
                <div>
                        This list is the <b>EXCLUDED</b> list. This means it will not try to extract these
                        sounds. If you want any of these sounds to be added to your project, you can click
                        on them and then hit the, 'Move,' button to move it to the included list.
                </div>
        """,

        "list_project": """
                <div style='font-size:14pt;'>Included RWAV Instructions</div>
                <div>
                        This list contains a bunch of instruction files. These instruction files
                        explain what RWAVs to extract from what indexes. They are given names to
                        represent what types of sounds they will extract. For example, 'Link Sound Effects,'
                        will extract all of Link's sound effects into your project BRWSD if included.
                </div>
                <br>
                <div>
                        This list is the <b>INCLUDED</b> list. Any instructions in this list
                        will be applied to your project when you click, '<b>Create SD Project BRWSD.</b>'
                        If you don't have anything in this list at all, you won't be allowed to press
                        that button because you would be creating an empty project. If you wish to remove
                        something from the included list, you can select the item then click the, 'Move,'
                        button to move it to the excluded list.
                </div>
                <br>
                <div>
                        If your project was created from the, '<b>Convert Modified SD WZSound to Project,</b>'
                        button, it will automatically have an instruction file with the name you gave.
                </div>
        """,

        "button_create_instructions": """
                <div style='font-size:14pt;'>Create Instructions</div>
                <div>
                        Creates a new instruction file that can be used to define what RWAVs should be
                        added to your BRWSD Project when included. You only need to create instructions
                        if there are currently no instruction files that extract the RWAVs you want.
                </div>
        """,

        "button_edit_instructions": """
                <div style='font-size:14pt;'>Edit Instructions</div>
                <div>
                        Allows you to edit an instruction file.
                        It will open an explorer window showing all the instruction yaml files. You can select
                        the yaml you want to edit. You only need to edit instructions if the instruction
                        file is not extracting all the RWAVs it should.
                </div>
                <br>
                <div>
                        Keep in mind that any DEFAULT
                        instruction files may be written over if you update the program. If you think
                        a default instruction file is not extracting everything it should, ask <b>@RayStormThunder</b>
                        in the SSR or SSHDR server and I will look into it.
                </div>
        """,

        "text_yaml_edit": """
                <div style='font-size:14pt;'>YAML Instructions</div>
                <div>
                        This is a YAML file that is used to tell the program what RWAVs to
                        extract from what indexes. If you go to the root folder, (The folder
                        that contains the exe,) you will see a folder called "Indexes."
                        This folder is a collection of BRWSD files with every RWAV from
                        the WZSound. You can open up any of these files with Brawlcrate
                        and listen to the sounds. It is important to note that when going
                        through indexes in brawlcrate, all RWAVs will have names of Audio[#]
                        where '#' is a number. As such, RWAVs will be referred to as Audio[#].
                </div>
                <br>
                <div>
                        There is some documentation of what sounds are in what indexes here: <br>
                        <a href="https://docs.google.com/spreadsheets/d/1DCLMLXRMok6Iyk0BDTjtdBkzT1k1zQvzSfZXEwR0kiE/edit?gid=1359457321#gid=1359457321">
                                InstructionPatcherIndex - Google Spreadsheet
                        </a>
                        <br>
                        You want to go to the tab called, 'InstructionPatcherIndex,' NOT the one called 'WZSoundIndex.'
                        This has some, but not all, documentation of what types of sounds are in that index. This can
                        make it easier to find specific sound effects.
                </div>
                <br>
                <div>
                        Sounds are extracted by stating an Index, like Index_005. Then giving a series of Audio[#] or
                        range of Audio[#] For example:<br><br>
                        Index_004:<br>
                            - 1<br>
                            - 3 - 7<br><br>
                        This will extract the Audio[#] 1, 3, 4, 5, 6, 7 from Index_004. You could also simply put "- All"
                        if you wish to extract everything from that Index.
                </div>
        """,

        "button_save_changes": """
                <div style='font-size:14pt;'>Save Changes</div>
                <div>
                        This will save the changes made to the yaml. If you were creating an instruction file, a new file
                        will show up in your list with the name you gave. If you were editing an instruction file, that file
                        will now extract audio based on your new yaml changes.
                </div>
        """,

        "button_cancel_changes": """
                <div style='font-size:14pt;'>Cancel Changes</div>
                <div>
                        Will discard all progress made. If you were creating an instruction file, no instruction file
                        will be created or show up in your list. If you were editing an instruction file, that file
                        will remain unchanged.
                </div>
        """,

        "button_create_brwsd": """
                <div style='font-size:14pt;'>Create BRWSD</div>
                <div>
                        Creates a new BRWSD file based on the current included RWAV Extraction Instructions.
                        This will look at the instructions that are included and extract all of those RWAVs
                        into a file called, 'your_project.brwsd.' You can then open up that file in Brawlcrate.
                        You can replace sound effects and save the project to come back to later.
                </div>
                <br>
                <div>
                        Once opened in Brawlcrate, you can listen to all the sound effects and then replace them
                        with the sound effects you think it should have. It is important to note that SIZE of the
                        sound effect can not be EQUAL to or GREATER than the sound effect you are replacing.
                        When you are clicked on a sound effect. You can see a field called, 'Uncompressed Size (Bytes).'
                        The file you replace it with must have a smaller size than that value.
                </div>
                <br>
                <div>
                        If you do replace a sound effect with a sound effect that is larger in size than the original,
                        my program will just not replace that and can even warn you about what sound effects are too large.
                </div>
        """,

        "button_load_brwsd_folder": """
                <div style='font-size:14pt;'>Load BRWSD Folder</div>
                <div>
                        This just opens the folder in which, 'your_project.brwsd' lies.
                </div>
        """,

        "button_create_wzsound": """
                <div style='font-size:14pt;'>Create WZSound</div>
                <div>
                        This will take whatever sound effects are in, 'your_project.brwsd,' and figure out at
                        what place in WZSound should that sound effect be inserted. Once it finds where every RWAV
                        should go. It will create a folder with every RWAV that is modified and not too large along
                        with an instruction file on where those RWAVs should be inserted at. Once completed, a window
                        will pop up showing you every RWAV that you haven't edited yet as well as every RWAV that was
                        too large. If there are any files that were too large, it will allow you to reset those sound effects
                        back to their original sound effects in the, 'your_project.brwsd,' file.
                </div>
                <br>
                <div>
                        The goal of this is to be able to easily and quickly patch the WZSound file with only the
                        RWAVs you are changing and a patch file. After this step is completed, '<b>Patch SD WZSound</b>,'
                        should be nearly instant.
                </div>
        """,

        "button_load_instructions_folder": """
                <div style='font-size:14pt;'>Load Instructions Folder</div>
                <div>
                        This just opens the folder in which, 'WZSoundPatchInstructions' folder lies.
                </div>
        """,

        "patch_sd": """
                <div style='font-size:14pt;'>Patch SD WZSound</div>
                <div>
                        This will insert the RWAV files from your project directly into the WZSound file
                        as described by the patch file. Because this does no searching, it should be
                        incredibly fast.
                </div>
        """,

        "patch_hd": """
                <div style='font-size:14pt;'>Patch HD WZSound</div>
                <div>
                        This will ask for the HD WZSound file if you haven't provided it before.
                        If you haven't provided it before, then it will also have to extract all the
                        indexes.
                </div>
                <br>
                <div>
                        It will then search the entire file for each unmodified RWAV file, and then
                        for each RWAV found, it will insert your modified RWAV at that location.
                        Due to the fact it has to search the entire 2GB file as many times as there
                        are modified RWAVs. This process can take awhile to complete.
                </div>
        """,

        "load_hd": """
                <div style='font-size:14pt;'>Load HD WZSound</div>
                <div>
                        This just opens the folder in which the HD, 'WZSound' file lies.
                </div>
        """,

        "load_sd": """
                <div style='font-size:14pt;'>Load SD WZSound</div>
                <div>
                        This just opens the folder in which the SD, 'WZSound' file lies.
                </div>
        """,

        "button_upload_sd_cutscene": """
                <div style='font-size:14pt;'>Upload SD Cutscenes</div>
                <div>
                        This asks for the "demo" folder which is located next to where the WZSound file is found in the game files. 
						It asks for SD version of the file. Once you give it the demo folder the program will now modify demo
						files and include it inside your output. 
                </div>
        """,

        "button_upload_hd_cutscene": """
                <div style='font-size:14pt;'>Upload HD Cutscenes</div>
                <div>
                        This asks for the "demo" folder which is located next to where the WZSound file is found in the game files. 
						It asks for HD version of the file. Once you give it the demo folder the program will now modify demo
						files and include it inside your output. 
                </div>
        """,

        "combo_allow_cutscene": """
                <div style='font-size:14pt;'>Allow Cutscenes</div>
                <div>
                        Allows your project to either respect the demo folder or not. If you Allow Cutscene Instructions then your project will
						contain sound effects from the Cutscene files. If you disallow it then your project will only be
						from the WZSound.
                </div>
        """
    }
