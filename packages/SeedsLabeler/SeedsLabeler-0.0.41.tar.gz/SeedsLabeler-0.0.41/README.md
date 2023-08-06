# Seeds Labeler

## Installation

Install the last version of SeedsLabeler with `pip install SeedsLabeler --upgrade`.

More details in [INSTALL.md](INSTALL.md).

## Run SeedsLabeler

In a terminal, simply run `SeedsLabeler`.

## Guidelines

For any modification request, open an issue.

Once the issue is solved, commit your changes with the message "Fixes #<issue_number>". The issue will be automatically closes at the next push/merge/deployement.

## Modify UI

TO update the user interface, modify `src/gui/mainwindow.ui` and recompile the equivalent python filw with 

`pyuic5 src/gui/mainwindow.ui -o src/gui/ui_mainwindow.py`

## [Dev] Update pip pacakge (requires admin rights for pip project and github repo)

Update [version.py](src/libs/version.py) with the new version number.

Make wure twin is installed: `pip install twine`

Run `python setup.py upload`.
