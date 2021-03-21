# trakt_sync
sync movies and shows from local hard disk to trakt using api

Officail API docs [here](https://trakt.docs.apiary.io/)<br/>
Official blog [here](https://blog.trakt.tv)

### Setup
You need to create a new application [here](https://trakt.tv/oauth/applications). Fill some random url
like `https://localhost:0000/` in `Redirect uri`, we won't be using that. Copy the client secret and client id that get
created and add them to **secrets.py** as required.

```bash
pip install -r requirements.txt
python auth.py #for authentication
python main.py #for sync
```

This code is highly specific, look at my [blog post](https://madhavtummala.github.io/blog/2021/03/21/syncing-hisotry-with-trakt.html)
to get a general idea of the API and code to develop something that works for you.
