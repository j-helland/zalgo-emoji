# zalgo-emoji
emoji-fied zalgo text using latex rendering

# Example
Paste the output of 
```
python zalgo-emoji.py -i "cool, thanks" -n 15 --font-size Large --emoji 😎 👍
```
into mattermost, making sure to wrap it in 
````
```latex
PASTE HERE
```
````

Suggestion: send yourself the message first to make sure it renders as expected. Occasionally, the script outputs things that the latex renderer doesn't like. 
