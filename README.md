# KnowledgeAI
KnowledgeAI is AI interface to your internal knowledge

To configure edit `.env` file in app directory and configure application.

If you want to go with OpenAI GPT backend you need to configure:</br>
`OPENAI_API_KEY="sk-..."`</br>
and perhaps:</br>
`GPT_MODEL="gpt-4"`</br>
(the app defaults to gpt-3.5-turbo)</br>


If you have a capable GPU you can change backend to MPT-7b with:</br>
`BACKEND="mpt7b"`</br>

Last but not least you can customize appearance with something like:
```
APP_NAME="Sauton AI"
TAGLINE="I've read all Tolkien's books. Ask me anything."
DATABASE="Tolkien.faiss"
```
of course you need to prepare the database first. (more on that later)