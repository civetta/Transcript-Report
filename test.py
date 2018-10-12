# -*- coding: utf-8 -*-
import unicodedata

all  = """See if you can use what we did to try this on your own.
You are doing a great job! Time to work on your own.
I think you have it from here! Keep up the awesome work!
I have not heard from you in a few minutes.
Please come back if you need more help. Have a nice day!
I understand why you think that, but let's look at this another way.
Let's look at that answer together to see if it works.
Your choice of words does not meet our chat rules. Please be respectful. Would you like my help with math?
I would like to help you. Are you ready to work on this together?
I am sorry that you do not want to work with me. Please come back when you are ready. 
It is okay if you do not know! We can work together to find out.
Please give it a try! It is okay to make mistakes.
It really helps to read or listen to the problem carefully. Please try that now.
Please tell me something you know from the problem.
I am sorry for the delay. Thank you for your patience!
Please give me a moment to look over your work. We will get started soon!
I am sorry you had to wait! Let's get started.
Yes, I am happy to help.
What do you already know that might be useful here? 
Do you have a headset or speakers so that I can talk to you?
We must not have a good audio connection today. Let's type!
I don't think you are able to hear me, but we can type!
Your device does not work with my mic for some reason. Let's type!
I am not able to switch your teacher, but I am happy to help you. Let's get started!
Please do not share personal information on the internet. Let's work on math!
That is personal information. Let's just stick to math!
I can only help you on Imagine Math. You can ask our teachers about your math questions here. 
That is not important right now. Are you ready to work on your math? 
We are going to practice with one of the parts in your problem, and then you can try without me. Ready? 
That is a very serious thing to say and I am sad to hear that you are in pain. I know that this can be really hard to deal with.
I have found it helpful to talk to someone when I am feeling sad or in pain. Have you tried talking to your teacher or a counselor at school about this? 
It's important to have people around you that know what is happening. I will let someone at your school know that you'd like to talk.  
Please consider chatting with a counselor at https://suicidepreventionlifeline.org/chat/ or by calling 1-800-273-TALK (8255). They are available anytime.
Are you okay?
I will alert your teacher. What is happening?
Have you talked to an adult about this?
I am sad to hear that you are dealing with this. I can let someone know for you.
Let's talk about your math problem first.  :)
The whiteboard is really cool, but the Imagine Math Teacher will decide when to use it.  :) 
Let's talk about your math problem first and then I will decide if we need to use it.  :) 
Thank you for the suggestion! It is helpful to hear other strategies that you are using in your classroom. Would you like me to continue this session?
We are always adding new content & revising existing content, so your feedback is really helpful! 
There are multiple ways to solve any math problem. It is important to us to help students understand how to approach a math concept or idea.
Since this is an instructional product, one of our goals is to introduce and teach new concepts. Therefore, we provide many forms of support, such as the Live Teachers! I would be happy to help your student understand this concept. 
Students work through problems in the Guided Learning and Practice activities before they complete the Quiz. If students have unfinished learning, they will receive scaffolded support to build confidence and experience success with the concepts.
Thank you for sharing your concern and I am sorry you are experiencing this issue!  Imagine Learning really appreciates your feedback. Unfortunately, I am unable to help with content or technical issues. Please contact our Customer Care at support@imaginelearning.com or 866-457-8776.
Let's take a look at an example together.
The Imagine Math Teacher can see the student's item, answer choices, and images. We use examples or other approaches to explain concepts and help guide the student through the problem solving process. We can also use the interactive whiteboard and other visual models to help the student develop a deeper conceptual understanding and work through problems independently.
What does this problem ask you to find?
I am not able to wait, but please come back when you are ready.
Did you hear my voice? 
Should I type or talk to you? 
How many correct choices does the problem tell you to select? 
I cannot speak in Spanish, but I can try to type in Spanish. Would you like me to do that for you?
Your teacher has **not** indicated that you need help in Spanish. Would you like me to ask your teacher to change this for you? 
No puedo hablar en español, pero podría escribir en español para ayudarte. ¿Estás de acuerdo con eso?   
Tu maestro **no** indicó que necesitas ayuda en español. ¿Te gustaría que me ponga en contacto con tu maestro para que ajuste tu cuenta y puedas recibir ayuda en español?
I am glad you clicked Chat Now to connect with a Live Teacher. I am here to help you. Are you ready to get started on your math? 
I am sorry you are not ready to work on your math. Please click **Math Help** and review the chat rules to work with an Imagine Math Teacher again. 
If you need more help, click the **Math Help** button and go to the *Imagine Math Teacher* tab. Have a nice day!"""



all = all.split('\n')
new_all=[]
for a in all: 
    import re
    b = re.sub(r'[^\x00-\x7F]+','',a).decode('utf-8','ignore').strip()
    c = str(b)
    new_all.append(c)
print new_all