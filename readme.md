<img src="screenshot.jpg" width="75%" height="75%" />

# processage v0.1

Processage embeds a secret message into a process tree and displays the processes in a shuffled table. Re-construct the process family tree to decode the secret message.

## Description

Understanding PIDs and PPIDS was challenging for my students, so I made processage to help with that (and for fun and to help me learn new things, too). The goal is to gamify learning about PIDs and PPIDs.

* Each character in the secret message is used as the name of a new process, which process is parented to the previous character's process.
* Linux
    * Sets process names in process tree (Try:  ps -ef | sort)
* Windows
    * Process names are available in processage and Windows Process Explorer, but not in Task Manager or via wmic.  For more info:
        * See [setproctitle](https://pypi.org/project/setproctitle/)
        * See [Windows Process Explorer](http://technet.microsoft.com/en-us/sysinternals/bb896653.aspx)
* At close, processage copies the shuffled process tree (game board?) to the clipboard and saves it as csv, html, and markdown..
    * Example output in shown in output.csv, output.md, and output.html.
    * Comment out lines 76-78 to disable saving output.
    * These files could be useful for constructing secret message worksheets.
* For fun, try using a shortened url as the secret message.

## Getting Started

### Cloning and Setup
```
mkdir processage
cd processage
python -m venv .
scripts\activate.bat
git clone https://github.com/FrozenBurrito/processage.git
pip install -r requirements.txt
```

### Running processage
```
python processage.py
```

## Help

Let me know if you have any questions or suggestions.

## Authors

Jon Morris, [frozenburrito](https://github.com/frozenburrito)

## Version History

* 0.1
    * It works!

## License

This project is licensed under the MIT License.  See the LICENSE.md file for details.

## Helpful Libraries

* [setproctitle](https://pypi.org/project/setproctitle/)