
prompt_INIT = """

You are an expert in parsing text files and representing the same information in a JSON file with a particular structure and based on guidelines. You think CRITICALLY and STEP BY STEP, checking AT EVERY STAGE that you followed the rules and did not make any mistake. 

"""


prompt_TEXT = """

<task>
Your task is to parse a text file with legal data and convert it to JSON file with a particular structure and following some guidelines.
</task>

"""


prompt_EXPLANATION = """

<task_explanation>
To accurately convert the structured text from the text file to the JSON file, it's crucial to understand both the source text file's structure and the target JSON file's desired format. This conversion process involves mapping the content from a linear, text-based format into a structured, hierarchical JSON format.

<structure_of_txt>
### Understanding the Structure of the text file
The text file is organized into a hierarchical structure of legal decrees, consisting of titles, chapters (if present), and articles. Each section starts with a header (e.g., "Título I", "Capítulo I", "ARTÍCULO 1.") followed by the relevant content. Titles are the highest level of this hierarchy, chapters (if present) are the next level, and articles are the lowest level. Each article is uniquely numbered and followed by its content, detailing specific decrees or law amendments.

</structure_of_txt>


<structure_of_json>
### Understanding the Structure of the json file
The json file aims to represent the same information as decreto.txt but in a structured JSON format. This format allows for a hierarchical representation, making the data easier to navigate and understand programmatically. The JSON structure consists of nested objects, each representing a title, chapter, or article. Each title object contains a "title" key with the title's name as its value and a "contents" key, which is an object containing either chapters or articles. Chapters, if present, follow a similar structure, with a "title" and "contents" key. Articles are represented as key-value pairs within the "contents" object, with the article number as the key and the article text as the value.
</structure_of_json>

<transition_from_text_to_json>
### Transition from the text file to the json file
1. Identify Titles: Start by locating the titles in the decreto.txt file, marked by a "Título" prefix. For each title, create a new object in the JSON file, assigning the title's name to the "title" key.

2. Identify Chapters: Within each title, identify chapters indicated by a "Capítulo" prefix. For each chapter, create a new object within the title's "contents" object in the JSON file, assigning the chapter's name to the "title" key and initializing a "contents" object for its articles.

3. Identify Articles: Articles are marked by an "ARTÍCULO" prefix followed by a number. For each article, create a key-value pair within the appropriate "contents" object in the JSON file (either directly within a title or within a chapter, depending on its placement in the text file), using the article number as the key and the article text as the value.

4. Maintain Hierarchical Structure: Ensure that the hierarchical structure is accurately represented in the JSON. Articles should be nested within their respective chapters (if present), and chapters should be nested within their respective titles.

5. Formatting and Cleanup: Properly format all text, removing unnecessary whitespace and escaping special characters in the article text that may interfere with the JSON format (e.g., double quotes).

6. Validation: Use a JSON validator tool to ensure the JSON file is correctly formatted and free from syntax errors after the conversion is complete.

</transition_from_text_to_json>

<notes_on_guidelines>
### Notes

- Ensure each "Capítulo" and "Título" has both a "title" and a "contents" key. The "contents" key is crucial for nesting "Artículos" or further "Capítulos".

- Avoid placing "Artículo" entries directly under "Título" or "Capítulo" without nesting them inside the "contents" object.

- Pay close attention to the nesting levels and maintain the original order of "Títulos", "Capítulos", and "Artículos".

- Use unique keys for each "Artículo" within its respective "contents" object and ensure all text is accurately represented.

By adhering to these guidelines and avoiding the outlined pitfalls, the conversion process from the text file  to the json file will be more accurate and structured, ensuring a faithful representation of the legislative document in JSON format.


</notes_on_guidelines>

</task_explanation>

"""



# Few-shot/CoT examples
prompt_EXAMPLES = """

<examples>
### Example 1: Basic Structure

#### Initial Content from text file

```
Título I - BASES PARA LA RECONSTRUCCIÓN DE LA ECONOMÍA ARGENTINA

ARTÍCULO 1.- EMERGENCIA. Declárase la emergencia pública en materia económica, financiera, fiscal, administrativa, previsional, tarifaria, sanitaria y social hasta el 31 de diciembre de 2025.
```
#### Final Result in json
```
{
  "Título I": {
    "title": "BASES PARA LA RECONSTRUCCIÓN DE LA ECONOMÍA ARGENTINA",
    "contents": {
      "Articulo 1": "EMERGENCIA. Declárase la emergencia pública en materia económica, financiera, fiscal, administrativa, previsional, tarifaria, sanitaria y social hasta el 31 de diciembre de 2025."
    }
  }
}

```

### Example 2: Title with Chapters

#### Initial Content from text file

```
Título II - DESREGULACIÓN ECONÓMICA

Capítulo I - Banco de la Nación Argentina (Ley N° 21.799)

ARTÍCULO 13.- Derógase el artículo 2° de la Ley N° 21.799.

```
#### Final Result in JSON File

```
{
  "Título II": {
    "title": "DESREGULACIÓN ECONOMÍA",
    "contents": {
      "Capitulo I": {
        "title": "Banco de la Nación Argentina (Ley N° 21.799)",
        "contents": {
          "Articulo 13": "Derógase el artículo 2° de la Ley N° 21.799."
        }
      }
    }
  }
}

```

### Example 3: Title with Mixed Articles and Chapters

#### Initial Content from text file

```
Título III – REFORMAS LEGISLATIVAS

ARTÍCULO 62.- MODIFICACIONES. Se introducen las siguientes modificaciones en el Código Civil y Comercial de la Nación.

ARTÍCULO 63.- APLICACIÓN. Las disposiciones de este título son aplicables a todas las relaciones y situaciones jurídicas existentes.

Capítulo I – Modificaciones al Código Penal

ARTÍCULO 64.- Se modifica el artículo 171 del Código Penal.

ARTÍCULO 65.- Se modifica el artículo 172 del Código Penal.
```
Título III – REFORMAS LEGISLATIVAS

```
{
  "Título III": {
    "title": "REFORMAS LEGISLATIVAS",
    "contents": {
      "Articulo 62": "MODIFICACIONES. Se introducen las siguientes modificaciones en el Código Civil y Comercial de la Nación.",
      "Articulo 63": "APLICACIÓN. Las disposiciones de este título son aplicables a todas las relaciones y situaciones jurídicas existentes.",
      "Capitulo I": {
        "title": "Modificaciones al Código Penal",
        "contents": {
          "Articulo 64": "Se modifica el artículo 171 del Código Penal.",
          "Articulo 65": "Se modifica el artículo 172 del Código Penal."
        }
      }
    }
  }
}
```


These examples demonstrate the correct structure for representing legislative documents in JSON format, with clear distinctions between titles, chapters, and articles, ensuring each element is properly nested and keyed according to the document's hierarchy.
</examples>

"""

prompt_DoNOTs = """


<do_NOTs>
# DO NOT?s

Here's a list of "DO NOTs" to avoid common errors when converting legislative text into a JSON structure:

- DO NOT omit the "title" and "contents" keys within each "Título" and "Capítulo". These are essential for maintaining the hierarchical structure.
- DO NOT place "Artículo" entries directly under "Título" or "Capítulo" without nesting them inside the "contents" object. Every "Artículo" must be a key-value pair within "contents".
- DO NOT ignore the nesting levels. Ensure that "Capítulos" are properly nested within "Títulos", and "Artículos" within "Capítulos" (if applicable) or directly under "Títulos" if they do not belong to any "Capítulo".
- DO NOT mix up the order of elements. Maintain the original order of "Títulos", "Capítulos", and "Artículos" as they appear in the text.
- DO NOT forget to use unique keys for each "Artículo" within its respective "contents" object. Each "Artículo" must be identifiable and accessible.
- DO NOT use inconsistent key naming. Stick to a consistent format for "Título", "Capítulo", and "Artículo" keys to avoid confusion and ensure uniformity.
- DO NOT include the "title" of a "Título" or "Capítulo" as a separate entry within "contents". The "title" should be a separate key-value pair outside of "contents".
- DO NOT disregard the importance of accurately representing the text of each "Artículo". Ensure that the content of each "Artículo" is correctly captured as the value for its key.
- DO NOT manually edit the JSON without validating it afterward. Always use a JSON validator to check for errors such as missing commas, unclosed brackets, or misquoted strings.
- DO NOT overlook the encoding of special characters. If the legislative text contains special characters (e.g., accents, symbols), ensure they are correctly encoded in the JSON file to avoid issues with character rendering.



By avoiding these common pitfalls, you can ensure a more accurate and structured conversion of legislative text into JSON format.

</do_NOTs>

"""


prompt_TXT = """

Below is the text file that you have to parse and convert into the structured JSON:

"""

prompt_FINAL = """

Output JSON file: 

"""