# Introduction to the Anthropic API

Source course (free after registration) [here](https://learn.deeplearning.ai/courses/building-toward-computer-use-with-anthropic).

## Getting an API Key

Go to [this link](https://console.anthropic.com/dashboard), click "Get API Key", and follow the instructions. Once you create the API key, you will be able to copy a long string. This string is shown to you by Anthropic **only once**. Copy it and keep it safely (if you lose it, no big deal, just delete it in the web interface and create another one).

Note: unfortunately the API is not free, even for PRO users. You have to add some money to your account to be able to use it.

## API file

The notebooks will assume that you have an API key (long string) and that you copied it in the `api.txt` file. This is just one way of doing it, you can also set it in your terminal before launching Jupyter, like so:

```bash
export 
```

Note: when working with GIT, you don't want accidentally to commit the file with your api key inside it. In order to prevent git from tracking changes inside it, run this command in your terminal from the root of this repository:

```bash
# https://stackoverflow.com/a/761116/9638108
# https://git-scm.com/docs/git-update-index#Documentation/git-update-index.txt---no-assume-unchanged
git update-index --assume-unchanged anthropic-api/api.txt
```
