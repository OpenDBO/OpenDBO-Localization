# OpenDBO-Localization
This repository holds text data for DBO. It contains both the original text and localizations for different languages.

## Status
Only the English translation is fully completed (100%) although it still contains errors and things to improve, specially in the parts that were translated long ago.

The other localizations are somewhat complete, but not fully.

## Contribute
Feel free to open Issues if you play in game and notice something that's wrong. Alternatively, you can simply edit the .xml file yourself, fix it, and submit a Pull Request.

# Tools
This repository include some tools.
- Find Chinese tool: this tool will simply detect which lines still contain Chinese characters and the total number of lines containing them.
- Parser tool: this tool is used to convert back and forth between .rdf and .xml. Example usages: `python parser.py text.xml --to-rdf --file-type text` and `python parser.py quest.rdf--to-xml --file-type quest`.

## License
All content is released under CC BY-SA. This means:
```
This license enables reusers to distribute, remix, adapt, and build upon the material in any medium or format, so long as attribution is given to the creator. The license allows for commercial use. If you remix, adapt, or build upon the material, you must license the modified material under identical terms. CC BY-SA includes the following elements:

BY: credit must be given to the creator.
SA: Adaptations must be shared under the same terms.
```

## Acknowledgements
We thank everyone who worked on translating the text in the past including (but not limited to) DBOCOM (and contributors), DBOG and Zenkai.