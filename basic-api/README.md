# Basic Api
Basic web server api running on Python Flask

```
Endpoint: [GET] <example.com>/api/hello?visitor_name="Mark"
```

Response: 
```
{
  "client_ip": "127.0.0.1", // The IP address of the requester
  "location": "New York" // The city of the requester
  "greeting": "Hello, Mark!, the temperature is 11 degrees Celcius in New York"
}
```