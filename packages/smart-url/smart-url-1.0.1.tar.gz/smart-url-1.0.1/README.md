# Smart Url: Simple url operations handler

---

*Smart Url* helps you to make simple operations in a string that represents a url or path,
such as change/append query, path or even anchor.


It also makes easy for you to:

1.  Get an object instance with useful attributes to consult separate parts of your url.

---

## Usage

#### Install

```
pip install smart-url
```

```
from smart_url import SmartPath, SmartUrl

path = SmartPath('GustavoBPereira/smart-url?doc=examle#usage')
url = SmartUrl('https://github.com/GustavoBPereira/smart-url?doc=examle#usage')
```

After pass a **url** to **SmartUrl** or a **path** to **SmartPath**,
you will have an object with attributes and methods that can be helpful
to handle with most common challenges when you are interacting with urls.

##### SmartPath atributes:
```
>>> path.anchor
'#usage'

>>> path.query
{'doc': 'examle'}

>>> path.path
'/GustavoBPereira/smart-url'
```


##### SmartUrl atributes:
Also all SmartPath atributes
```
>>> url.host
'github.com'

>>> url.port
None

>>> url.protocol
'https'

>>> url.is_secure
True

>>> url.netloc
'github.com'
```


##### You can change the atributes values and call str(url) to have the url representation with that state, for example:

```
url = SmartUrl('https://github.com/GustavoBPereira/smart-url')
url.path = 'another/path'
>>> str(url)
'https://github.com/another/path'
```

### But, you have methods to perform operations like that and can be more intelligent to use them.

#### Methods available to both classes:


> update_query
>> Receive a dict and perform an update in your query dict


> change_query
>> Receive a dict and change your query dict

> append_path
>> Receive a str and make an sanitized append in your path atribute

> change_path
>> Receive a str and make an sanitized change in your path atribute

> change_anchor
>> Receive a str and make an sanitized change in your anchor atribute


---

## Example of usage?
```
from smart_url import SmartUrl

my_url = SmartUrl('https://github.com/GustavoBPereira/smart-url')
my_url.update_query({'is_an_example': True})
my_url.change_anchor('#usage_example')

>>> str(my_url)
'https://github.com/GustavoBPereira/smart-url?is_an_example=True#usage_example'

if my_url.query.get('is_an_example', False):
    print('you get an url with is_an_example parameter :)')
else:
    print('This is not an url with is_an_example parameter :(')

>>> you get an url with is_an_example parameter :)
```
---

## License

MIT License

Copyright (c) 2022 Gustavo Brito Pereira

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
