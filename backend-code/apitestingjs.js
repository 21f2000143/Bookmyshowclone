// to validate the @auth_required
fetch("http://127.0.0.1:8000/get/venue", {headers:{"Content-Type": "application/json", 
'Authentication-Token': 'WyI4ODZiMGRmYjljN2U0ZGRiYmVlZmJmOTMxNTBjZWFkNSJd.ZJG1ZA.78QaoxhiRuh8LW2CyM85hlyE3as'}})
.then(response=>response.json())
.then(data=>console.log(data))

// for login
let data={"email":"sk9666338@gmail.com", "password": "password"}
fetch("http://127.0.0.1:8000/login?include_auth_token", {headers:{"Content-Type": "application/json"},
method:'POST', body:JSON.stringify(data)})
.then(response=>response.json())
.then(data=>console.log(data))
// next to continue https://youtu.be/4NSW7IM8Sr4?t=1382
// fetch api using cookies
fetch("http://127.0.0.1:8000/get/venue", {credentials:"same-origin",})
.then(response=>response.json())
.then(data=>console.log(data))