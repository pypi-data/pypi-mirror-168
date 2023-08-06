# Guard that provide exclusive access to an object  

Python 3.7 or higher.

**Install**: pip install asyncio-guard

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/inyutin)


### Examples of usage:
1. Set a value, get exclusive access to it, set another value
```python
guard = Guard(obj=1)

async with guard as obj:
    assert obj == 1

await guard.set(2)
async with guard as obj:
    assert obj == 2
```

2. Update a value by using update function.  
This update function will be used, if no value was set up.
```python
guard = Guard(obj=1, update_func=lambda: return 2)

async with guard as obj:
    assert obj == 1

await guard.update_func()
async with guard as obj:
    assert obj == 2
```
