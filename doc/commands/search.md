# Search

Search for Work items on the Polarion Server.
The query must be in the Polarion format.

Example:

```cmd
pyPolarionCli --user my_username --password my_password --server my_server search --project my_project --query "author.id:myname"

```

Try the search command by executing the [batch file](/examples/search/search.bat).

## FAQ

### Working with Documents

The JSON output of the queries does not include much information on the documents in which the Work items are found. There are a couple of ways to use the queries and existing data to achieve your goals:

1. `location` field: This field provides an URI to the location in which the Work Item is found. If you know the structure and names of the spaces and their documents, you can extract the information from this string.
    - Get the location: `--field location`

2. `document.title`: It is possible to make queries for the key `document.title`, eventhough it does not belong to the Work Items. For example:
    - Work items without a document: `-q "NOT HAS_VALUE:document.title"`
    - Work items in a specific document : `-q "document.title:DOCUMENT_TITLE"`

The underlying library for Polarion in Python provides more possibilities for [working with documents](https://python-polarion.readthedocs.io/en/latest/document.html), and these can be implemented in pyPolarionCli if the feature is requested in an [Issue](https://github.com/NewTec-GmbH/pyPolarionCli/issues).
