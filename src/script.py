import fire
import openai
import json


def generate(
    input_file: str,
    translations_file: str,
    title: str,
    tex_output_file: str,
    api_key: str,
    model: str = "gpt-3.5-turbo",
    original_language: str = "Wenyan",
    translation_language: str = "English",
):
    print(f"{original_language} -> {translation_language}")
    openai.api_key = api_key
    with open(input_file) as f:
        lines = f.readlines()
        lines = [l for l in lines]
    print(f"A total of {len(lines)} units...")
    sections = []
    for l in lines:
        sections.append({"original": l})
    prompt = f"Translate the following {original_language} into {translation_language}:"
    for s in sections:
        print("Processing: " + s["original"])
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt + s["original"]},
            ],
        )
        s["translation"] = response["choices"][0]["message"]["content"]
    print(f"Translations completed... dumping into {translations_file}")
    with open(translations_file, "w", encoding="utf8") as f:
        json.dump(sections, f, ensure_ascii=False)

    print("Generating tex file...")
    tex_document = ""
    with open("tex_header.txt") as f:
        contents = f.read()
        tex_document += contents
    for section in sections:
        tex_document += "\\begin{pairs}\n\\begin{Rightside}\n\\begin{[TOK:MAIN]}\n\\beginnumbering\n\\pstart\n"
        tex_document += section["original"]
        tex_document += (
            "\n\\pend\n\\endnumbering\n\\end{[TOK:MAIN]}\n\\end{Rightside}\n"
        )
        tex_document += (
            "\\begin{Leftside}\n\\begin{[TOK:TRAN]}\n\\beginnumbering\n\\pstart\n"
        )
        tex_document += section["translation"]
        tex_document += "\n\\pend\n\\endnumbering\n\\end{[TOK:TRAN]}\n\\end{Leftside}\n\\end{pairs}\n\\Columns\n"
    tex_document += "\\end{document}"
    tex_document = tex_document.replace("[TOK:MAIN]", original_language)
    tex_document = tex_document.replace("[TOK:TRAN]", translation_language)
    tex_document = tex_document.replace("[TOK:TITLE]", title)
    with open(tex_output_file, "w") as f:
        f.write(tex_document)
    print("Done.")


if __name__ == "__main__":
    fire.Fire(generate)
