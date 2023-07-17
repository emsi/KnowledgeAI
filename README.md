# KnowledgeAI - Your AI Interface to Internal Knowledge

Welcome to KnowledgeAI, your personal Artificial Intelligence interface to internal knowledge. This guide will help you set up and configure the application according to your needs.

## Configuration

To configure the KnowledgeAI application, you'll need to edit the `.env` file located in the
`app` directory.

### Available Settings

Here are the settings you can customize:

```markdown
BACKEND: Choose between "chat_gpt" (default) and "mpt"
```

#### For OpenAI GPT Backend:

If you prefer to use the OpenAI GPT backend, you need to set the following configurations:

```markdown
OPENAI_API_KEY: Your OpenAI API Key, e.g. "sk-..."
MODEL: Specify the model, e.g. "gpt-4" (the application defaults to "gpt-3.5-turbo")
```

#### For MPT Backend:

If you have a capable GPU, you can switch the backend to MPT and set the model as follows:

```markdown
BACKEND: Set to "mpt"
MODEL: Specify the model, e.g. "mosaicml/mpt-7b-instruct"
```

### Application Appearance

You can also customize the application's appearance by changing the following settings:

```markdown
APP_NAME: Your application name, e.g. "Sauton AI"
TAGLINE: A brief description or tagline, e.g. "I've read all Tolkien's books. Ask me anything."
DATABASE: The database to be used, e.g. "Tolkien.faiss"
```

Please note that you'll need to prepare the database in advance.
More information on this will be provided later.
