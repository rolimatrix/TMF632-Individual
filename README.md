# TMF632-Individual
TMF632 Individual build with Flask

I created this Implementation only to extend my development Expertise.
Motivated from my Job as Lead Business Architect inside German Telecom IT. There I work as responsible Architect for Giga.

One of my actual Task is to design TF632 Individual Solution in use for Giga. Not for Enterprise!!!
I reduced orinal TMF 632 based Schema to our need. Example Language ability is not part of this Solutin. Also GET Methode for Endpoint Host/Individual/. 
See swagger in Folder /conf/swagger.

On 1.6.2021: Patch Method is not yet build and not all Schema are implemented.
I have Contacts, Characters. Next i will implement related Party, skill and external Reference.

I used Flask and Flasgger. Flasgger only to have Swagger UI available for that Flask APP. When App is runnig you can call  
http://host/apidocs (Example: http:://localhost:5000/apidocs) to study and try execution for documented endpoints.

In case that you want to try this Python App, make one GIT Clone. After that create one OS Env. Variable with Name DATABASE_URL.
There but in you path and credential to you local or remote DB.
I used local Postgress. Example:"postgresql+psycopg2://<Username>:<Password>localhost:5432/DBName"

Then go to Terminal and type in following 3 Command:
1. FLASK DB INIT
2. FLASK DB MIGRATE
3. FLASK DB UPGRADE

=> look on you Database. You will see 7 Tables from APP. One Alembic Table.
Then start APP.
Then start Postman. You can import Party postman.collection.json and try POST/GET/DELETE.

Kindly regards Roland
