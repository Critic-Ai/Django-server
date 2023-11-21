## Local Server

### Instructions:

1) replace the clusterurl in `myapp/views.py`

2) in the root folder run the following command:


```
python manage.py runserver
```

3) run the llm_server docker container by using the following command from an **elevated container**:

```
docker build -t llm_server ./llm
docker run -it -p 2023:2023 --gpus all llm_server
```