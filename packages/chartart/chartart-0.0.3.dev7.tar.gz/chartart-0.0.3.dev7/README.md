# ChartArt Package is under development

Use 
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

Change Log 

0.0.1 => 0.0.2 
Added support for =>
-Publish post without javascript package from notebook
-Pulish post from standalone python script (Non jupyter environment)


0.0.2 => 0.0.3 
Added support for features at the time of publishing post. Features will get used as filters.

0.0.3.dev5 => 0.0.3.dev6
-Support for status posts compatible with new low code platform.
Example: 

```

filters = {
    "dateAdded": datetime.datetime.now().isoformat() + 'Z',
    'rowSubscriptionCol': 'vendor',
    'type': 'aggregatePost'
}

data = {
    'count': 5,
    'status': 'Warning',
    'vendor': 'GCP'
}

post = Post(postId='GCP_aggregatePost', postTitle='# Aggregated Post')
post.addFilters(filters)
post.createPost(data=data)

```
0.0.3.dev6 => 0.0.3.dev7
-Added Exception handling code if response is not in json format