


  <h3 align="center">MdiskPro</h3>

  <p align="center">
   A Unofficial Wrapper for Mdiskpro.xyz
    <br />
    ·
    <a href="https://t.me/DKBOTZHELP">Report Bug / Request Feature</a>
    ·
    <a href="#usage">Usage</a>
    ·
    <a href="#reference">Reference</a>
  </p>
</div>


---

# MdiskPro
An Unofficial Python version of Mdiskpro.xyz. Used to Short your long link and let you Earn from it.


## Installation

Install shortzy with pip

```bash
pip install mdiskpro
```
    
To Upgrade

```bash
pip install --upgrade mdiskpro
```
    
    
## Usage

```python
from mdiskpro import MdiskPro
import asyncio

mdiskpro = MdiskPro('<YOUR API KEY>')

async def main():
    link = await mdiskpro.convert('https://example.com/')
    print(link)

asyncio.run(main())
```

```python
Output: https://mdiskpro.in/mVkra
```


## Features

- Single URL Convert
- Batch Convert from List
- Convert from Text

## Contributing

Contributions are always welcome!

## Reference

### Init
```python
from mdiskpro import Shortzy
import asyncio

mdiskpro = MdiskPro(api_key="Your API Key") 

```

### Convert a single URL

```python
convert(link, alias, silently_fail, quick_link) -> str
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `link` | `string` | **Required**. Long URL Link |
| `alias` | `string` | Custom alias for the link |
| `silently_fail` | `bool` | Raise an exception or not if error ocuurs |
| `quick_link` | `bool` | Returns the quick link |


Example:

```python
async def main():
    link = await mdiskpro.convert('https://www.youtube.com/watch?v=d8RLHL3Lizw')
    print(link)

asyncio.run(main())

```

### Convert from Text

```python
convert_from_text(text:str, silently_fail:bool=True, quick_link:bool=False) -> str
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `text`      | `str` | **Required**. Text containing Long URLS to short|

Example:

```python
async def main():
    text = """
Unstoppable:-https://www.youtube.com/watch?v=330xlOv8p9M
Night Changes:-https://www.youtube.com/watch?v=syFZfO_wfMQ
"""
    link = await MdiskPro.convert_from_text(text)
    print(link)

asyncio.run(main())


```

### Get quick link

```python
get_quick_link(link:str)
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `link`      | `str` | **Required**. Long Link|

Example:

```python
async def main():
    link = "https://www.youtube.com/watch?v=syFZfO_wfMQ"
    quick_link = await MdiskPro.get_quick_link(link)
    print(quick_link)

asyncio.run(main())

```

## Credits
 - [Thanks To Me](https://T.ME/DKBOTZHELP)
