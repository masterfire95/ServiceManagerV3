# ServiceManagerV3

## Description:
With this tool you can monitor, start and stop Windows Services on multiple hosts. You can create several configurations and call them up via a selection.
For example, you can create a configuration with which only the Exchange Windows service can be managed and a second configuration for the Windows services of an SQL server.

## How to:
Use ServiceManagerSelection.py to start the program.
You can add a new configuration with the Add button. Here you have to enter Name(of the config), AutoRefresh (y/n), RefreshTime(s) and RowsPerColumn(e.g. 3 services then in the next column). Finally, click on Add Service and add hostname and service name. Then click on Create ServiceList. A <name>.json is now created in the ServiceLists folder (can be changed in the config.json file). 

Now you can choose your config in the selection and should see the previously defined services.

The prerequisite is that the user has the appropriate authorization on the server.

Translated with DeepL.com (free version)
