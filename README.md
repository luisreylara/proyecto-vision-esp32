 # Ejecutar el docker compose, se ejecuta automáticamente el main.py , verificarlo con el comando ```ps -x```

 ```
docker compose up -d 
```
 
 # Se puede crear la imagen con este comando

```
docker build -t app-vision:1.0.0 . -f Dockerfile

```


 # forma 1 para crear el contenedor e ingresar en este

```
docker run -it -p 5000:5000 app-vision:1.0.0 sh

```
 # forma 2 de crear el contenedor en modo -d 
```
docker container run --name app-vision -dp 5000:5000 app-vision:1.0.0
```

# ingresar el contenedor 

```
docker exec -it app-vision sh
```