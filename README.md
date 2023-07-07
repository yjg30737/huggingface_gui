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

## Method Overview
When you selects certain model in the table, `onModelSelected` signal of `HuggingFaceModelWidget` will be sent.
`onModelAdded`, `onModelDeleted` are supported as well. self-explanatory i believe.

When you set the cache directory with "cache directory" above the table, `onCacheDirSet` signal will be sent.

While using `HuggingFaceModelTableWidget`, you can show specific headers only by `setHorizontalHeaderLabels` as like QTableWidget.

But i overrided the function so there is only 4 labels possible: "Name", "Size", "Text2Image?", "Visit"

You can get `HuggingFaceModelClass` class with `getModelClass` from HuggingFaceModelWidget. You can install or delete certain model and get size of every model in current cache directory. You can do such things with one line.

Others:

* `getModelTable()` - get the model table widget
* `selectCurrentModel(model_name)` - set the row including "model" in the table as current one
* `setText2ImageOnly(f: bool)` - if you want, you can show text2image models only with and you can set the cache directory with `setCacheDir` in `HuggingFaceModelClass`.
## How to Run
1. git clone ~
2. pip intsall -r requirements.txt
3. python huggingFaceModelWidget.py

## Preview
![image](https://github.com/yjg30737/huggingface_gui/assets/55078043/fa67e162-c193-42b9-9d83-9d39957ca2d6)

## How to Use
Press "Add" button to add new model. Dialog will pop up. You can enter the model name you want to install.

After you successfully install the model, dialog will close and you can see the installed model in the current model tables.

If installation is not successful, error message box will pop up.  

Press "Delete" button will delete the selected model on the table.

You can see the total sizes of the huggingface model you installed from the bottom of the table.
