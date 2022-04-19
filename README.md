# Tom-necesita-ayuda

## Descripción

Tom es estudiante de ciencias de la computación y se encuentra estudiando una misteriosa dirección websocket que encontró en un profundo foro de internet que le planteaba un reto a todos los lectores, que de lograrlo, descubriría la identidad de nada más ni nada menos que de Satoshi Nakamoto.
El funcionamiento de este stream websocket es muy simple: consiste en conectarse y recibir cada 100 ms 100 JSON diferentes con la misma estructura:

```console
{
“a”:1 // Rango[1-100]
“b”:0 // Rango[0-2^32]
}
```
Tom analizando se dio cuenta de algo, de un patrón, y es que si organizamos los datos de cierta forma, se podía conseguir información muy valiosa que nos ayudaría a completar el reto. Tom piensa que el parámetro “a” representa un índice y el “b” es un número sacado de una secuencia numérica extraña y desconocida, el cual aún no conoce la fórmula. Por ello, creó un sistema de 100 bloques de información con igual estructura que contenía un resumen de un minuto, con el comportamiento de los valores que se obtenían de “b”. La estructura usada es la siguiente:

```console
struct {
_max_number;
min_number;
first_number;
last_number;
number_of_prime_numbers;
number_of_even_numbers;
number_of_odd_numbers;
}
```

- El primer dato representa cuál fue el número mayor obtenido de “b” en ese periodo de tiempo.
- El segundo, el número menor.
- El tercero, el primer número obtenido.
- El cuarto, el último.
- El quinto es un contador que nos dice cuántos de esos números fueron números primos.
- El sexto, otro contador pero de cuantos fueron números pares.
- El séptimo, un contador que nos dice cuántos números fueron impares.

Tom necesita recolectar toda esa información en los diferentes bloques e imprimirlos cada vez que pase un minuto y luego reiniciarlos, para seguir procesando nuevos datos venideros, esto le servirá para analizar su comportamiento a través del tiempo. Pero tiene un problema, Tom a pesar de ser un estudiante de ciencias de la computación ¡no sabe programar! Entonces nos pide su ayuda, ¿estás dispuesto a ayudar a Tom?

## Recursos:
ws://209.126.82.146/ (Misteriosa dirección websocket aportada por misterioso usuario en el extraño foro que retorna los datos anteriores explicados)
