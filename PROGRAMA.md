# Cómo publicar el programa del sábado

El programa (quién está encargado de cada parte) vive en el archivo **`programa.json`**.
En el sitio aparece como una tarjeta junto a los horarios, y **desaparece solo cuando la fecha ya pasó**.

## Para actualizarlo cada semana

1. Abre https://github.com/iasdlaslomas/iasdlaslomas.github.io/edit/main/programa.json
2. Cambia la `fecha` al sábado que viene (formato `AAAA-MM-DD`).
3. Cambia los nombres de los encargados (los datos vienen del Excel que comparten — solo copia los nombres).
4. Puedes agregar o quitar partes: cada una va entre llaves `{ }` separada por comas.
5. Botón verde **Commit changes** dos veces. En 1–2 minutos se actualiza el sitio.

## Formato de cada parte

```json
{ "hora": "11:40", "parte": "Mensaje", "encargado": "Pr. Nombre Apellido" }
```

- `hora` es opcional (si no la pones aparece un punto).
- **Comillas dobles** siempre, coma entre partes pero **no** después de la última.
- Verifica el formato en https://jsonlint.com si algo no aparece.

> 💡 Tip: también puedes pegarle el programa de Excel a Claude y pedirle
> "conviértelo al formato de programa.json de iasdlaslomas.com" — te lo devuelve listo para pegar.
