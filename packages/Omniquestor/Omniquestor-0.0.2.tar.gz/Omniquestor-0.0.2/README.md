Omniquestor
 
A simple utility for handling auth header python requests.

Instantiate the class with a url, an auth header token, and a request type of get, post, put, or delete.
Then save the response by calling the response() function.
Example usages:

`endpoint_url = www.example-site.com/auth`
`auth_header = "Authorization": "Bearer <token value>"`

`get_example_omniquestor = Omniquestor(endpoint_url, headers=auth_header, request_type="get")`
`get_example_response = get_example_omniquestor.response()`

For requests with an item id be sure to include it in the endpoint_url:

`get_item_url = www.example-site.com/01`
`post_item_url = www.example-site.com/01`
`put_item_url = www.example-site.com/01`
`delete_item_url = www.example-site.com/01`

Then usage is the same as above:

`put_item_example_omniquestor = Omniquestor(endpoint_url, headers=auth_header, request_type="put")`
`put_item_example_response = put_item_example_omniquestor.response()`
