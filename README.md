# pyqt_huggingface_gui
Manage HuggingFace models with Python desktop app

Maybe it's only me but managing HuggingFace models is kind hard job to do, especially someone who is not friendly with CUI.

This app let you install and delete any huggingface models (as far as i know) with a GUI.

## Requirements
* PyQt5 >= 5.14
* huggingface_hub
* transformers

## How to Run
1. git clone ~
2. pip intsall -r requirements.txt
3. python huggingFaceModelWidget.py

## Preview
![image](https://github.com/yjg30737/pyqt_huggingface_model_table/assets/55078043/60fe68a9-7ff3-4d2a-9970-c5c071c83dbe)

## How to Use
Press "Add" button to add new model. Dialog will pop up. You can enter the model name you want to install.

After you successfully install the model, dialog will close and you can see the installed model in the current model tables.

If installation is not successful, error message box will pop up.  

Press "Delete" button will delete the selected model on the table.

You can see the total sizes of the huggingface model you installed from the bottom of the table.
