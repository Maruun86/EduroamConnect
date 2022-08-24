Functions
=========
Here you will find an overview of all the functions in the script and what they are doing.

.. py:function:: main()

    Controlls the script main function

    :param: NONE
    :return: BOOL


.. py:function:: IsSUDO()

    Try to create a fooEdu folder in /etc to check if script is started with SUDO rights.

    :param: NONE
    :return: BOOL


.. py:function:: AddOrRemoveEntry()

    A simple welcome text and question for the next step, a choice between Adding configuration to the system or removing Username/Password

    :param: NONE
    :return: BOOL


.. py:function:: InputUser()

    Allows the Input for a Username, and uses the DOMAIN to match it with the Username

    :param: NONE
    :return: string


.. py:function:: InputPassword()

    Allows the Input for a password

    :param: NONE
    :return: string


.. py:function:: HasRightDomain()

    Checks if the username has the right DOMAIN

    :param: NONE
    :return: BOOL


.. py:function:: CheckAddInterfaces()

   Checks the /etc/network/interfaces, if it does not exist it creates one with the configuration of the entryString

    :param: NONE
    :return: NONE


.. py:function:: CheckAddWPA()

     Checks the /etc/wpa_supplicant/wpa_supplicant.conf if it does not exist it creates one with the configuration of the entryString and entryString2

    :param: NONE
    :return: NONE


.. py:function:: ModifyWPAAuth()

     Modifys the identity and password entry in the network block inside of the wpa_supplicant.conf

    :param username: username that needs to be changed/added
    :param password: password that needs to be changed/added
    :return: NONE


.. py:function:: WriteIntoFile(overwrite = false)

    Is a function to write a string into a file.

    :param filepath: Example: "/etc/wpa_supplicant/wpa_supplicant.conf"
    :param entryString: Example: "Hello World"
    :param overwrite: OPTIONAL: completely overwrites the file.
    :return: NONE


.. py:function:: CheckAddTimeServer()

    Checks the /etc/systemd/timesyncd.conf for the correct TIMESERVER entry and changes it when nessesary

    :param: NONE
    :return: NONE


.. py:function:: AskForReboot()

     Needs user confirmation for a reboot otherwise it will just close the script

    :param: NONE
    :return: NONE