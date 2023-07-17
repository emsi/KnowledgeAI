# KnowledgeAI - Your AI Interface to Internal Knowledge

Welcome to KnowledgeAI, your personal Artificial Intelligence interface to internal knowledge. This guide will help you set up and configure the application according to your needs.

## Configuration

To configure the KnowledgeAI application, you'll need to edit the `.env` file located in the
`app` directory.

### Available Settings

Here are the settings you can customize:

```markdown
BACKEND="chat_gpt" (default setting), or BACKEND="mpt"
```

#### Using OpenAI GPT Backend

If you choose to utilize the OpenAI GPT backend, please configure the following:

```markdown
OPENAI_API_KEY="sk-..."
MODEL="gpt-4"
```
Please note that if `MODEL` is not specified, the application will default to `"gpt-3.5-turbo"`.

#### Using MPT Backend

If you have a capable GPU, you can switch the backend to MPT and set the model as follows:

```markdown
BACKEND="mpt"
MODEL="mosaicml/mpt-7b-instruct"
```

### Customizing Application Appearance

You can also customize the application's appearance by changing the following settings:

```markdown
APP_NAME="Sauton AI"
TAGLINE="I've read all Tolkien's books. Ask me anything."
DATABASE="Tolkien.faiss"
```

Please note that you'll need to prepare the database in advance.
More information on this will be provided later.
