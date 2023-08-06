# SOCO-SEARCH Plugin Helper

# soco-plugin-library

```
pip install soco-search-plugin
```

## How to create a source distribution
```
python setup.py sdist
``` 


Twine is for the upload process, so first install twine via pip:
```
pip install twine

```

Then, run the following command:
```
twine upload dist/*
```


## How to run grpc server
```
python3 -m soco_grpc.server --host 0.0.0.0 --port 8003 --workers 3
```

## how to run http server
```
# main.py
import uvicorn
if __name__ == "__main__":
    uvicorn.run("soco_grpc.server.app.server.app:app", host="0.0.0.0", port=8006, reload=True)

```
