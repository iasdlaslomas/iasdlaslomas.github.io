# Cómo publicar anuncios en iasdlaslomas.com

Los anuncios del sitio viven en el archivo **`anuncios.json`** de este repositorio.
Para editarlo solo necesitas una cuenta de GitHub con acceso (no hay que instalar nada):

1. Abre https://github.com/iasdlaslomas/iasdlaslomas.github.io/edit/main/anuncios.json
2. Edita el contenido (mira los ejemplos de abajo).
3. Presiona el botón verde **Commit changes** dos veces.
4. En 1–2 minutos el sitio se actualiza solo.

## Formato

Cada anuncio va entre llaves `{ }`, separado por comas, dentro de los corchetes `[ ]`:

```json
{
  "etiqueta": "Este sábado",
  "titulo": "Bautismos y Santa Cena",
  "detalle": "Te esperamos en el culto de las 11:00.",
  "enlace": "https://ejemplo.com",
  "boton": "Ver detalles",
  "estilo": "accent",
  "hasta": "2026-08-15"
}
```

| Campo | ¿Obligatorio? | Qué hace |
|---|---|---|
| `titulo` | Sí | El texto principal del anuncio |
| `etiqueta` | No | Texto pequeño arriba del título (ej. "Este sábado") |
| `detalle` | No | Una línea de descripción |
| `enlace` + `boton` | No | Agregan un botón con liga |
| `estilo` | No | `accent` (azul), `ink` (oscuro) o `tint` (claro). Si se omite, se alternan |
| `hasta` | No | Fecha límite `AAAA-MM-DD`; después de ese día el anuncio desaparece solo |

## Reglas de oro

- **Comillas dobles** `"` siempre, y **coma** entre anuncios (pero NO después del último).
- Si el archivo queda vacío así: `[]` — la sección de anuncios se oculta del sitio.
- Si algo sale mal y la sección desaparece, revisa que no falte o sobre una coma.
- Puedes verificar el formato pegando el contenido en https://jsonlint.com

## Anuncios con imagen (diseños de Canva)

Si el anuncio tiene un diseño hecho en Canva:

1. En Canva descarga la imagen como **JPG** (calidad estándar es suficiente).
2. En GitHub: **Add file → Upload files** y sube la imagen (ej. `semana-oracion.jpg`).
3. En `anuncios.json` agrega el campo `"imagen"` al anuncio:

```json
{
  "titulo": "Semana de oración",
  "detalle": "Del 21 al 27 de julio, 19:30.",
  "imagen": "semana-oracion.jpg",
  "hasta": "2026-07-27"
}
```

La imagen aparece como miniatura dentro del anuncio.
