# 1. Introduce

​	This is a concise and user-friendly Python interface that can be used to populate PDF forms. Simply upload any PDF form to be filled, and construct a dictionary corresponding to the filling data, and you can generate a filled PDF.

# 2. Install

* Make sure the following commands are executed within a virtual environment.
* The latest version of pymupdf 1.23.8 has fixed the issue with `button_state()`, so it is recommended to upgrade to the latest version if possible.

```
pip3 install -r requirements.txt
```

* If you are unable to upgrade to the latest version, you can apply a patch to fix the `button_state()` function in older versions.

```
make patch
```

# 3. Develop
```python
import filler  # Import directly assuming that the project root directory has been appended to sys.path
handler = filler.Filler(name)  # 'name' refers pdf files to be filled
handler.fill(value)  # 'value' is the dictionary before conversion
handler.export()  # Specify the path to export the PDF, default is "output/<name>.pdf"
```

# 4. Test
1. Original JSON data format (key format passed to the Filler class): `test/pre_convert`.
```
make pre-test
```
2. Converted JSON data format (key format based on the PDF configuration): `test/post_convert`.
```
make post-test
```
3. Automatically generate `field.json` and test data.
```
make automator TERGET="<name>"
```

# 5. Notice
1. Modifying the default values of the PDF: a. Edit `default.json`; b. You can use any PDF editor (including Adobe Acrobat) to modify the corresponding `template.pdf` file.
2. Warning in vscode at the import location: It can be ignored. The warning is due to the dynamically imported `convert` function, which will not cause any runtime errors.
