 # crear contenedor

```
docker build -t app-vision:1.0.0 . -f Dockerfile

```



 # ejecutar

```
docker run -it -p 5000:5000 app-vision:1.0.0 sh

```
 # ejecutar

```
docker container run --name app-vision -dp 5000:5000 app-vision:1.0.0
```

# ejecutar

```
docker exec -it app-vision sh
```