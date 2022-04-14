# wagtail-placeholders
RichText editor feature to allow for inserting placeholder tags via a static list displayed in a modal.

In the UI, this feature is called "Template Tags" and the tool Icon for it is "<Tt>", but "template" and "tag" were too generic in the code I wrote this for, so it's called "placeholders" in the code itself.

**Files:**
- ```urls.py``` Contains the code required to load the placholders endpoint which loads the modal template selector.
- ```views.py``` Loads the modal template. It contains a hard-coded list of 'demo tags' that can be replaced with the placeholders you need for your project. Alternatively, copy this up into your project's views file and write in your own hard-coded list of templates, or load them from another model or API.
-  ```wagtail_hooks.py``` Registers the feature into the text editor. Here is where we set the 'icon' in the editor's toolbar to '<Tt>' and register the custom JS for this plugin.
- ```static/.../placeholder.js``` React code that handles the UI rendering of placeholders. Also sets endpoint to hit to load the modal - this should match what's set in urls.py (the receiving end).
- ```templates/.../placeholders_modal.html``` The HTML template used to load the placeholder selection modal.

**Install:**
1. Add wagtail-placeholders directory into your project
2. Add wagtail-placeholder to your INSTALLED_APPS (base.py)
3. Enable the feature on a text block: ```RichTextBlock(features=["placeholders"])```


Editor with Template Tag chosen:
![Alt text](RichText1.png?raw=true "RichText Editor")

Template Tag chooser modal (with demo tags):
![Alt text](RichText2.png?raw=true "Placeholder Modal")
