# Welcome to the Circuit user manual

## Overview of Circuit

**Circuit** is a social network where you can write posts with 256 characters to specified groups called *circles*.

## Get started with Circuit

### FAQs

### Signing up

If you don't have a **Circuit** account, you can sign up for one in a few steps:

1. Go to the **Circuit** website
2. Click the "Sign up"-button in the upper left.
3. Now fill out your email address, a username, a secure password and double-check all entries.
5. Click the blue "SIGN UP"-button.
6. Once you sign up, you'll need to confirm your email address.
Therefor follow the link in the email you just received.
7. You are now on the login page. Please enter your username and password.
8. Finally you can see your profile!

#### Having troubles?

+ Is your email address used for another account already? It's not possible to use this email address again.
+ Maybe there is already someone using the same username. Try another one!
+ Still not working? Please take a look at the chapter **Troubleshoot** or contact the **Circuit** team.

### Logging in
If you already have a **Circuit** account, you can log into your account by clicking the "Login"-button in the upper right.

#### Forgot your password?
Click the "Forgot password?"-button and enter your email address. The system will send you a message with a link to a password reset site.

Please enter a new password. Now you can login with your new password!


### How to post
If you are logged in you can easily write a post in the field "Write something!".
For further information what you can do with posts please take a look at **Posts** below.

### How to find people

### How to use circles
In your profile you will find a button that is called `Manage circles`. There you can edit, create, and delete circles.
For further information, just keep reading until you get to **Circles** section.

### Glossary of terms
In our network you may be confronted with several new terms:

+ *Post*: Posts are the heart of **Circuit**. They are limited to 256 characters and you can write them for all your followers or just for a specified group called circle.
+ *Circle*: If you post something you can decide which group of people (circle) shall see it. You can easily create, delete and edit circles. Your circles are only important for you. So no other can see how you have grouped your followers. 

### Further help and contact details
If there are any further questions please first search for answers in this manual.
At last you can still contact the **Circuit** team by writing to the following email address:

support@circuit.io

## Manage your account

### Edit your profile
As every social network, you want kinda personalize your own profile! As we are minimalistic, and surely you are too, we have added only the minimal personalizable items as your name, your real name, your e-mail address, and a brief description of you.
You can, however, have your password changed or your account deleted if you would wish to. Just follow the instructions below and the job it's done!

### Change your password
Do you want to change your password? That's not a problem! Just go to your **profile**, click in ``Edit profile` and there you will find the area where you can easily change your password!
It takes only 1 minute!

### Delete your account
Had enough of social networking or you just haven't time enough? Well you can delete your account. Even if we would like to have you forever in our system, we can understand that you want to leave us.
To make that, just go to your **profile**, click in ``Edit profile``, go to ``Delete account`` section and click in the big red button.

    Once you delete your account, you cannot ``ctrl+z`` this action. So please think twice before doing this!

## Posts

### General informations
Posts are the heart of **Circuit**. It is the way you communicate with other users. There are some more options besides posting 256 characters of pure text. You can further answer to people, repost things, mention users or use hashtags.

With the help of our functions you can easily group information contained in your post and group for whom should it be.

### Hashtags
Hashtags are the best way to keep information centralized. If you want to highlight some information about your post, you just need to write a # followed by alphanumeric characters, and we'll do the rest!

You can look for all the posts that include that hashtag. To do that, just click on the hashtag you want or in the search field type # and the hashtag name you want to search for.

### Mentions
Mentions is one of the ways you can interact with people. You can let someone know that you want their attention if you write their username with a @ before it and he will get notified that you have mentioned him.

### Repost
You liked a post of another user? You liked it so much that you want to share it to your feed without stealing it? Just repost it! The reposts are really useful when you find a post that you would like to share with other people without writing it yourself!

### Favorite
You liked a post so much that you would like to have a quick access to it? Well that's what the **favorite** option is for! Just favorite a post, and keep an eye on it once in a while!

Once you've favorited you can quickly access to them from your profile!

## Circles

### Create a circle

### Edit your own circle

### Delete a circle

## Discover
You will soon have the option to search for other users, hashtags or circles!


## Connecting



## Policy



## Privacy



## Security



## Developers

## API
Do you want to connect with us from an external client? That's cool! We offer two possibilities to do that, via JSON and via HTML. Both of them are made considering the REST architecture styles.

### JSON API
Do you want to handle the info yourself? We are cool with that and we offer you an API that will always give you a JSON response.

#### General
If you want to see the information everytime without having to come here and read it again, we have made a general overview JSON Response where you can either look it up on our site or just send a request to
    [http://127.0.0.1/api/](http://127.0.0.1/api/)
and it will return what you can do.

#### Login
To login you have to send a GET request to
    [http://127.0.0.1/api/login/](http://127.0.0.1/api/login/)
get the field names and send back a POST request with the required fields. You will get a **Token**, *without it you won't get further*.

#### Send a post
To send a post you need to include in the header the given token as
    Authorization: Token <<token>>
You will need as well a post content, an image file or None if you don't want to upload one and **very important** a circle id. We will give you obviously which are the available circles that you can choose.

#### Restrictions
As we want to keep our servers spam-free, we've limited the requests that can be made via our API to 5 per minute if you're not logged in and 100 per day if you are a logged in user.

### HTML API
You don't want to worry about handling information and all that boring stuff? We have a solution for you! Use our HTML API! All you have to do to begin is to send a request to
    [http://127.0.0.1/api/login/](http://127.0.0.1/api/login/)
as a form request and you'll get a form! With which all the required info will be sent.

#### Login
After you send the first request, you'll get a form with a Log in form, fill the spaces and send the next request!

#### Send a post
All you've got to do is write the information, select your circle and **ba-dam-pts** your post was sent!

#### Restrictions
As we want to keep our servers spam-free, we've limited the requests that can be made via our API to 5 per minute if you're not logged in and 100 per day if you are a logged in user.

### GitHub
You want to see the magic under the hood? This is an open source project, so you can go to our GitHub site and see what's actually going on in here.
Want to come to visit the silicon chip of our circuit? Come to [visit us](http://github.com/7Pros/circuit)

### Admins

## Troubleshoot

### Bugs?
We are humans! It can come to times where our circuits get mixed and you see the resulting short circuit. You find a bug in our social network? You help us out and tell us which one.

To do that:
```
1. Go to our [GitHub repository](https://github.com/7Pros/circuit/).
2. Open our Issues.
3. Check if your bug is not already there.
4. If yes, just write in it that you're experiencing the same problem and suscribe to the thread so we can update you when we've fixed it.
5. If not, open an issue describing the bug and we'll back to you if we need any more information.
```