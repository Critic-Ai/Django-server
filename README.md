# Backend

Setup instructions

## MongoDB

1) replace the clusterurl in `myapp/views.py`

2) in the root folder run the following command:


```bash
python manage.py runserver
```

## LLM
Two ways:

### Local
1) dont
2) see llm/installscripts

### Docker
1) In llm/server.py set `ISDOCKER = True` and change `PORT` if needed
2) In an **elevated terminal**:

```bash
docker build -t llm_server ./llm
docker run -it -p 2023:2023 --gpus all llm_server
```

TODO:
- refactor /llm to latest version of llamaindex
- fix output of zephyr
