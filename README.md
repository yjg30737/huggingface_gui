# huggingface_gui
Manage HuggingFace models with Python desktop app

Maybe it's only me but managing HuggingFace models is kind hard job to do, especially someone who is not friendly with CUI.

This app let you install and delete any huggingface models(even Stable Diffusion model) with a GUI.

You can also change the path where you can download the model files (such as large binary(.bin) files).

For example, if you don't have enough space on your main drive, you can install them on a different drive.

Note: Some of the models could not be installed. Please tell me specific model if that happens.

## Requirements
* PyQt5 >= 5.14
* huggingface_hub
* transformers
* diffusers

## How to Run
1. git clone ~
2. pip intsall -r requirements.txt
3. python huggingFaceModelWidget.py

## Preview
![image](https://github.com/yjg30737/huggingface_gui/assets/55078043/8b7e9e1b-734f-4d0d-b707-a6bfb4566aaa)

## How to Use
Press "Add" button to add new model. Dialog will pop up. You can enter the model name you want to install.

After you successfully install the model, dialog will close and you can see the installed model in the current model tables.

If installation is not successful, error message box will pop up.  

Press "Delete" button will delete the selected model on the table.

You can see the total sizes of the huggingface model you installed from the bottom of the table.
