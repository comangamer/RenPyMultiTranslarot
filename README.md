# RenPyMultyTranslarot

+ What is it for?

This is a small project I needed at one time to automate the machine translation process for a RenPy game. It has a number of features of its own.

Let's put it this way. I have no idea what people usually write here, so I will try to describe how this code works, describing the task for which it was created.

In my project on the RenPy engine, I did manual translation from Russian to English. As a result, I had the original version and the English version. However, players asked me to add translations into many other languages that I don't know. So I wrote this script.

It takes as a basis the English version of the translation, which has a structure:

```
# game/script03.rpy:42
translate english chapter3_4616039d:

    # "Очередной солнечный день."
    "Just a regular sunny day."
    
# game/script03.rpy:87
translate english chapter3_02a1d108:

    # l "Накосячил? О чём это ты, Нени?"
    l "Guilty? What are you talking about, Neny?"

# game/script03.rpy:219
translate english serazgo_55278443:

    # n "Сераз, поздоровайся с посетителями…"
    n "Seraz, greet the visitors…"

translate english strings:

    # script03.rpy:116
    old "Сказать правду"
    new "Tell the truth"
```

This includes:
- The original string number with a # sign
- A string with the translation language and hash of the string
- Original phrase in Russian with # sign
- Translated phrase in English without # sign

Executing the script causes the original script file to look like this

```
# game/script03.rpy:42
translate german chapter3_4616039d:

    # "Очередной солнечный день."
    # "Just a regular sunny day."
    "[Translated text english->german]"
    
# game/script03.rpy:87
translate german chapter3_02a1d108:

    # l "Накосячил? О чём это ты, Нени?"
    # l "Guilty? What are you talking about, Neny?"
    l "[Translated text english->german]"

# game/script03.rpy:219
translate german serazgo_55278443:

    # n "Сераз, поздоровайся с посетителями…"
    # n "Seraz, greet the visitors…"
    n "[Translated text english->german]"

translate german strings:

    # script03.rpy:116
    old "Сказать правду"
    # new "Tell the truth"
    new "[Translated text english->german]"
```
In other words, the program adds a # sign to a line with English translation and creates a line below with translation into the selected language.
The program takes RenPy syntax into account as much as I needed it to. It takes into account the names of the characters speaking, it takes into account possible variables within lines of text enclosed in square brackets, like [current year] or {w} pharase separation.

# How to use? (.py and .exe)
- Copy the folder with the translation to English and change its name to the target language. Let it be 'french' as an example
- Place the file "translate CD v11.exe" (or “translate CD v11.py”) in the 'french' folder containing the .rpy files of English translations
- Run the program (Use f.e. IDLE Shell for .py script)
- The program will prompt you to select the target language (in our case french).
- The program will offer you to replace 'translation english' with 'translation french' (I recommend you to agree, so you don't have to change it yourself).
- The program offers you the choice to translate a specific file or all files in the folder (I recommend to translate all files at once).
- During the work the program DOES NOT REWRITE the original files, but saves all translated files in the 'french' subfolder. When finished, you can manually move them with replacement.

Important note: The program uses Google Translate machine translation. As a consequence, the translation may not be accurate. If quote characters are present in the original text, they may corrupt the final code. You need to fix this yourself (usually a couple of three lines)

+ Note

I'm not a programmer and I don't guarantee that this is the most ingenious and correct method of realizing the task. Nevertheless, it works fine for me, so I decided to share it with other RenPy developers to make this hard work easier.

Thanks for your attention and good luck with your development!
