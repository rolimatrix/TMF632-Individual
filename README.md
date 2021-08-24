# TMF632-Individual
TMF632 Individual build with Flask

I created this Implementation only to extend my development Expertise.
Motivated from my Job as Lead Business Architect inside German Telecom IT. There I work as responsible Architect for Giga.

One of my actual Task is to design TF632 Individual Solution in use for Giga. Not for Enterprise!!!
I reduced original TMF 632 based Schema to our need. Example Language ability is not part of this Solution. Also GET Methode for Endpoint Host/Individual/. 
See swagger in Folder /conf/swagger.

I implemented Contacts, Characters and related Party. 

I used Flask and Flasgger. Flasgger only to have Swagger UI available for that Flask APP. When App is runnig you can call  
http://host/apidocs (Example: http:://localhost:5000/apidocs) to study and try execution for documented endpoints.

In case that you want to try this Python App, make one GIT Clone. After that create one OS Env. Variable with Name DATABASE_URL.
There but in you path and credential to you local or remote DB.
I used local Postgress. Example:"postgresql+psycopg2://<Username>:<Password>localhost:5432/DBName"

Then start APP. DB Shema will be created automated in case that DB is not existing.

=> look on you Database. You will see 5 Tables from APP. One Alembic Table.

Try API out with  Postman. You can import Party postman.collection.json and try POST/GET/DELETE.
PATCH is yet not implemented.

Kindly regards Roland
