<p align="center">
  <img width="200" src="gradio-discord.jpg">
</p>

# The Gradio Discord Bot<sup>BETA</sup>

The Gradio Discord Bot is a way to use any [Hugging Face Space](https://hf.space) as a Bot from within your Discord server -- *all without writing any code*.

Below, we show examples how to use the Bot in your server to:

- 🌎 Translate between languages
- 🗣️ Convert text to speech
- 🔢 Do math calculations
- 🖼️ Generate images

All for free and without having to code anything!

## Installation

Installing the Gradio Discord Bot is very simple:

1. Copy and paste the following link in your browser: https://discord.com/api/oauth2/authorize?client_id=1040198143695933501&permissions=294406716480&scope=bot  

2. Choose which Discord server you'd like to add it to (you must have permissions to add Bots to that server of course)

<p align="center">
  <img width="600" alt="image" src="https://user-images.githubusercontent.com/1778297/208466659-00b23d23-fdc1-48e7-8868-dd248510acce.png">
</p>

3. Accept the permissions for the Gradio Bot

<p align="center">
 <img width="600" alt="image" src="https://user-images.githubusercontent.com/1778297/208466719-a6d64e0e-3aa1-4ead-90fc-23480f441b90.png">
</p>

* You can confirm that the Gradio Discord Bot has been successfully installed in your server by going to the server and seeing if there is an account with the name `@GradioBot` in your server:

<p align="center">
<img width="517" alt="image" src="https://user-images.githubusercontent.com/1778297/208510477-7a634158-885f-4083-981a-483d19ae7416.png">
</p>

4. (Optional) If you would like to use `@GradioBot` in a private channel, then you must add `@GradioBot` to that channel. In Discord, you can do this by right-clicking on the channel name, and then selecting ‘Edit Channel’. Then, go to ‘Permissions’ and select ‘Add a Role’ and find `@GradioBot` 


## Usage

Now that the Gradio Discord bot is installed, here's how to use it in any any channel in your Discord server:

1. From the channel, tag `@GradioBot` followed by the name of a Space you'd like to try,
such as `abidlabs/en2fr` ([a Space](https://huggingface.co/spaces/abidlabs/en2fr) that translates from English to French) or `abidlabs/speak` ([a Space](https://huggingface.co/spaces/abidlabs/speak) that converts text to spoken speech), or any of the more than 5,000 Gradio demos on [Hugging Face Spaces](https://hf.space). 

<p align="center">
<img width="446" alt="image" src="https://user-images.githubusercontent.com/1778297/208513251-5ba2e8bc-82e6-4037-995b-dfbba0720126.png">
</p>

2. Once you press enter, you'll notice that the name of GradioBot will change to reflect the name of the Space that it has loaded:

<p align="center">
<img width="572" alt="image" src="https://user-images.githubusercontent.com/1778297/208517352-ca167539-c78a-4226-9cd1-c8fe6c1a2645.png">
</p>

3. Now type in the input you'd like to pass into the Space. In this example, we'll pass in an English phrase: "Hello, friends." The input **must be enclosed in double-quotes**. Otherwise, it will be interpreted as the name of a new Space that you are trying to load. Once you 

<p align="center">
<img width="438" alt="image" src="https://user-images.githubusercontent.com/1778297/208517591-f8024af3-fa2e-41e4-b043-994c4ce5693b.png">
</p>

4. If you'd like to load a new Space, just type in the name of a new Space (without any quotation marks) and `@GradioBot` will load the new Space instead. If you'd like to reset to the initial state of the `@GradioBot`, you can type in "@GradioBot exit".

We'll show how to use `@GradioBot` with a few more complex Spaces below:

## More examples

### 🗣️ Convert text to speech (`abidlabs/speak`)

The `@GradioBot` can handle media as well as text. For example, [this Space](https://huggingface.co/spaces/abidlabs/speak) converts text to speech recordings. Here's how to use it:

1. In a channel, type `@GradioBot abidlabs/speak`

2. Then, type in some text *in quotation marks* that you'd like to convert to speech, such as `@GradioBot "Look at this cool demo!"`. You should see an audio file returned by `@GradioBot`: 

### 🔢 Do math calculations (`abidlabs/calc`)

The `@GradioBot` can handle Spaces that take multiple inputs. For example, [this Space](https://huggingface.co/spaces/abidlabs/calc) takes in two numbers and a mathematical operation. Here's how to use it:

1. In a channel, type `@GradioBot abidlabs/calc`

2. Then, type in `@GradioBot `, followed by a number in quotation marks, followed by a space, then a mathematical operation in quotation marks, followed by a space, followed by a number in quotation marks. Here's how it looks: 


### 🖼️ Generate images (`abidlabs/images`)

Here's another example that shows that `@GradioBot` can handle media. Using [this Space](https://huggingface.co/spaces/abidlabs/speak) converts text to images. Here's how to use it:

1. In a channel, type `@GradioBot abidlabs/images`

2. Then, type in some text *in quotation marks* that you'd like to convert into an image, such as `@GradioBot "an astronaut riding a horse"`. You should see an image file returned by `@GradioBot`: 


## Contributing

The Gradio Discord Bot is completely open-source. Feel free to open issues or pull requests in this repo to make it better!
