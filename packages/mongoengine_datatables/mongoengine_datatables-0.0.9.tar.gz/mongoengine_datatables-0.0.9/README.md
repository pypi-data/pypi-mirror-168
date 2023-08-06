# mongoengine datatables
A script for using the jQuery plug-in DataTables server-side processing with MongoEngine.

Works with Flask and Django. Supports column sorting and filtering by multiple search terms. Supports ReferenceFields & EmbeddedDocumentField for search.

[![Downloads](https://pepy.tech/badge/mongoengine-datatables)](https://pepy.tech/project/mongoengine-datatables)

###  Install
You can install with pip:

```bash
pip install mongoengine_datatables
```

###  Minimal example mongoengine datatables 
Copy paste this code to app.py
```python
from flask import Flask, render_template_string, jsonify, request
from flask_mongoengine import MongoEngine
from mongoengine_datatables import DataTables
app = Flask(__name__)
db = MongoEngine(app)


class Hello(db.Document):
    field_one = db.StringField()
    field_two = db.StringField()


@app.route('/api/', methods=['POST'])
def api():
    args = request.get_json()
    res = DataTables(Hello, args).get_rows()
    return jsonify(res)


@app.route('/')
def hello_world():
    if not Hello.objects(field_one='Hello').first():
        Hello(field_one='Hello', field_two='World').save()
    return render_template_string(
        '''
    <html> <head>
        <link rel="stylesheet" type="text/css"
        href="https://cdn.datatables.net/v/bs4-4.1.1/jq-3.3.1/jszip-2.5.0/dt-1.10.20/b-1.6.1/b-html5-1.6.1/r-2.2.3/sc-2.0.1/sl-1.3.1/datatables.min.css"/>
    </head>
    <body class="p-3">
          <table id="dt_table" class="table table-striped" style="width:100%">
            <thead>
            <tr>
                <th>one</th>
                <th>two</th>
            </tr>
            </thead>
        </table>
    </body>
    <script type="text/javascript"
        src="https://cdn.datatables.net/v/bs4-4.1.1/jq-3.3.1/jszip-2.5.0/dt-1.10.20/b-1.6.1/b-html5-1.6.1/r-2.2.3/sc-2.0.1/sl-1.3.1/datatables.min.js"></script>
    <script>
        $(function () {
            $('#dt_table').DataTable({
                serverSide: true,
                ajax: {
                    url: '{{ url_for('api') }}',
                    dataSrc: 'data',
                    type: 'POST',
                    contentType: 'application/json',
                    data: function (d) {
                        return  JSON.stringify(d)
                    }
                },
                columns: [
                    {data: 'field_one'},
                    {data: 'field_two'},
                ]
            });
        });
    </script> </html>
        '''
    )


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
```

Install modules & run:

`python app.py`

Results:

![](https://habrastorage.org/webt/so/ug/yg/sougygusqikirtcmjkzowk_yzmu.png)

### Advanced usage:
**embed_search** - For specific search in EmbeddedDocumentField
**q_obj** -  Additional search results in reference collection
**custom_filter** - Your custom filter

`DataTables(your_model, request_args, embed_search={}, q_obj=[], custom_filter={})`

### For datetime field
DataTables  return datetime as  epoch time with milliseconds. Example:

`{'my_date': {'$date': 1605116909954}}`

You can convert it:
```python
import time
time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(1605116909954/1000.0))
```

