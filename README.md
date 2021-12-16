<h1 align = "center" >FormActions </h1>
<p align="center">
<img height=50% width=50% src="https://socialify.git.ci/sanjibansg/FormActions/image?description=1&language=1&name=1&owner=1&theme=Light" />
</p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;
![License: MIT](https://img.shields.io/github/license/sanjibansg/FormActions)
![Repository Size](https://img.shields.io/github/repo-size/sanjibansg/FormActions)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
</br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
 [![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

<h5 align="center"> Microservice for simplified forms creation and robust actions triggering.
</h5>

-----
### Project Overview  
FormActions provides a simplified API interface for forms creation and actions triggering. It supports features for fast data access, scheduling actions, and robust actions and data handling.

----


### Instructions to run
FormActions can be simply used by running via the docker image
```
cd FormActions/
docker-compose build
docker-compose up
```
The API service will be running on port 84, from where API calls can be made for form & questions creation, action registration, answers & responses creation.

---------

### Technical Description
#### Web Framework
FastAPI
#### Database Management System
Apache Cassandra
#### Scheduling & enqueuing actions
Redis

---------

### Contributions  
For existing bugs and adding more features open a issue [here](https://github.com/sanjibansg/FormActions/issues)

----------
### License
[MIT License](LICENSE)

 ----
