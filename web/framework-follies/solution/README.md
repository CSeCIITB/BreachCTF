# Framework Follies

We are given a Next.js app along with its source. On extracting the source files and poking around, we can see that there are around 100 different randomly generated routes in the `src/app` directory.

On inspecting some of the files, its not clearly evident where the flag is being exposed from. There doesn't seem to be any mention of a flag.
However, one interesting thing to notice is that one of the directories stands out as it has a different size than all the others, the `src/app/ioEYWhJqZO` directory.

So we should now head into this directory and check out its contents. And as expected, we can see that there are some **Next.js Server Actions** being used and one of them is exposing the flag (spelled using leet speak: `f14g` which is why we couldn't find it initially). However, this server action doesn't seem to be used anywhere. It is however imported in the `page.tsx` file.

Now doing some preliminary research on Next.js Server Actions and some of the common vulnerabilities with them, we can figure out that though the action isn't being used anywhere, since it is marked as `"use server"` and it is imported in the `page.tsx`, it will be exposed by Next.js via a REST API endpoint.

We can also see that there is another server action that doesn't do anything but is being called by a button (hidden button) in the page. This can help us in figuring out how call the server action REST APIs. Pressing the button and monitoring the network activity, we can see that there is a bunch of stuff being sent. However, the `Next-Action` field stands out and looks like an identifier for the server action. But how do we get the action ID of the server action that returns the flag?

First thing that would come to mind is to look at the source sent to browser. But the code has been obfuscated! This makes it difficult to directly examine and figure out the action ID for the other server action. A clever method would be to do a regex search for the pattern that the server actions are generated as (a quick search can help you get this!). And voila, there are two matches in the file for this route (`816774ae6365211070941018e74c474ec` and `27cb19eb91692fce6e188119e76dc4ccbd21679d`) and since one of them was for the dummy action, the other one has to be the one for the action that returns the flag!



`Breach{d0nt_tru57_fr4m3w0rks_bl1ndly}`
