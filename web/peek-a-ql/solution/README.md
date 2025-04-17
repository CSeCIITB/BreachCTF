# Peek-a-QL

Even before looking at the challenge, we can make a pretty good guess from the name and that this is a web challenge that there will be some involvement of GraphQL.

Now getting into the actual challenge, we can see that the challenge is a sourceless one. So we should probably begin by looking at the source sent to the browser. But since we have some idea about the challenge from the name, we can skip this part and directly head to inspecting the network requests (though you could definitely figure this out by looking at the source sent to the browser as well).

First thing that one can notice is the requests being made to the `/graphql` endpoint. So we can try to check if GraphQL introspection is turned on or not. And to no one's surprise, it is on. So let's run the standard GraphQL introspection queries.

> [!TIP]
> You can read more about GraphQL introspection [here](https://graphql.org/learn/introspection/)

Running those queries would reveal that there is a `posts` query which returns an `author` field which has the `User` type. Interestingly, the `User` field has a `password` field.

Also on running the posts query, we can see that there is a post by the admin user. Via this we can get the admin password and login as admin.

```gql
query {
    posts {
        id
        title
        cont ent
        author {
            username
            password
        }
    }
}
```

Logging in as admin reveals the flag!

`Breach{gr4phql_1snt_s0_s3cur3_4ft3r_4ll}`
