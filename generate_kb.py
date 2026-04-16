import re

resume_path = "/home/kenton/Documents/Praxis/raw_resume.txt"
harvest_path = "/home/kenton/Documents/Praxis/deep_harvest_data.txt"
interview_path = "/home/kenton/Documents/Praxis/interview_responses.txt"
output_path = "/home/kenton/Documents/Praxis/knowledge_base.md"

with open(resume_path, 'r') as f:
    resume = f.read()

with open(harvest_path, 'r') as f:
    harvest = f.read()

with open(interview_path, 'r') as f:
    interview = f.read()

# I will craft the markdown text manually in Python to ensure perfect adherence.
md = """# Knowledge Base: Kenton Smeltzer

## Voice Profile & Philosophy
- Values scientific backed practices on teams.
- Uses the CIA's Animal Kingdom model for assembling highly dynamic teams to great effect.
- Values mentoring and considers force-enabling and building people to be an often undervalued skill.
- Believes an employee could be the worst technical employee but if they hire and force-enable the best in the industry to go 10x faster, they would be a company MVP.

## Relational Skills Database

### Node.js (Node)
- Utilized in full stack development toolchains at DexCare to deliver healthcare solutions.
- Used in AI agent development via NodeRED at DexCare.
- Managed team of 15 developers utilizing Node.js for front and web-service technologies at Joint Interagency Task Force.
- Strong hands-on experience designing and developing web applications at Lowbush Company.
- Endorsed as a skill on LinkedIn.

### Golang (Go)
- Utilized in full stack development toolchains at DexCare.
- Tech Stack for Allele: Modular Genetic Micro-Trading Engine.
- Endorsed as a skill on LinkedIn.

### Python
- Utilized in full stack development toolchains at DexCare.
- Endorsed as a skill on LinkedIn.

### Kubernetes
- Extensive use at DexCare to deliver healthcare solutions.
- Utilized at DexCare to design and develop ephemeral developer environments.
- Endorsed as a skill on LinkedIn.

### RabbitMQ
- Extensive use at DexCare to deliver healthcare solutions.
- Endorsed as a skill on LinkedIn.

### Postgres (PostgreSQL)
- Extensive use at DexCare to deliver healthcare solutions.
- Used for long-term genetic trait storage in Allele HFT engine.
- Endorsed as a skill on LinkedIn.

### Splunk
- Extensive use at DexCare to deliver healthcare solutions.
- Endorsed as a skill on LinkedIn.

### DataDog
- Extensive use at DexCare to deliver healthcare solutions.
- Endorsed as a skill on LinkedIn.

### Retool
- Utilized for AI agent development at DexCare.

### Grok/GPT API
- Utilized for AI agent development at DexCare.

### NodeRED
- Utilized for AI agent development at DexCare.

### n8n
- Utilized for AI agent development at DexCare.

### Rancher Desktop
- Utilized at DexCare for on-machine technology clustering to spin up ephemeral developer environments.

### React
- Managed team using React for front and web-service technologies at Joint Interagency Task Force.
- Strong hands-on experience designing and developing web applications at Lowbush Company.
- Endorsed as a skill on LinkedIn.

### Clojure
- Managed team using Clojure for big data and integration work at Joint Interagency Task Force.
- Endorsed as a skill on LinkedIn.

### Ethereum
- Blockchain development for Ethereum at Joint Interagency Task Force.
- Gained significant knowledge of Ethereum Smart Contracts, implementation details, and security weaknesses at Joint Interagency Task Force.
- Interfaced traditional technologies with Ethereum's blockchain at Joint Interagency Task Force.
- Endorsed as a skill on LinkedIn.

### Smart Contracts
- Helped design tooling and build smart contracts to trace black market activity at Joint Interagency Task Force.
- Gained significant knowledge of implementation details and security weaknesses at Joint Interagency Task Force.
- Endorsed as a skill on LinkedIn.

### Java
- Middleware development and strong hands-on experience at Lowbush Company.
- Hands-on development and oversight at Marriott Vacation Club.
- Used for custom software development at Body International.
- Hands-on development at Modis Technologies.
- Endorsed as a skill on LinkedIn.

### C#
- Designed systems using C# at AccessUSA (Hotelbeds).
- Hands-on development for Orlando.com / Internet Vacations.
- Endorsed as a skill on LinkedIn.

### C++
- Hands-on development of simulation software at Modis Technologies.
- Endorsed as a skill on LinkedIn.

### Dojo
- Strong hands-on experience at Lowbush Company.
- Built many of the Dojo-based modules for the IBM Jam web application.
- Provided a Dojo-based UI to display and aggregate conference content for IBM Social Media Aggregator (SMA).
- Hands-on work at Marriott Vacation Club, converting web-reservation system to modern browser application.
- Endorsed as a skill on LinkedIn.

### Architecture (Enterprise Architecture)
- Enterprise Architect / CTO at Lowbush Company.
- Provide and produce architecture requirements for Marriott Vacation Club.
- Executive decision-making on architecture at AccessUSA (Hotelbeds).
- Executive technology planning and architecture for Orlando.com.
- Endorsed as a skill on LinkedIn.

### Blockchain
- Blockchain development for Bitcoin, Ethereum and Monero at Joint Interagency Task Force.
- Helped design tooling and build smart contracts to trace black market activity on various blockchains.
- Endorsed as a skill on LinkedIn.

### Microservices
- Endorsed as a skill on LinkedIn.

### Kafka
- Endorsed as a skill on LinkedIn.

### Redis
- Used for ultra-fast caching in Allele HFT engine.
- Endorsed as a skill on LinkedIn.

### Docker
- Endorsed as a skill on LinkedIn.

### GCP
- Endorsed as a skill on LinkedIn.

### AWS
- Endorsed as a skill on LinkedIn.

### React Native
- Evaluated seed-stage technical stacks as Technical Advisor at StartX.
- Endorsed as a skill on LinkedIn.

### Vue
- Evaluated seed-stage technical stacks as Technical Advisor at StartX.
- Endorsed as a skill on LinkedIn.

### Redux
- Endorsed as a skill on LinkedIn.

### WebSockets
- Evaluated seed-stage technical stacks as Technical Advisor at StartX.
- Endorsed as a skill on LinkedIn.

### gRPC
- Evaluated seed-stage technical stacks as Technical Advisor at StartX.
- Endorsed as a skill on LinkedIn.

### CI/CD
- Endorsed as a skill on LinkedIn.

### Jenkins
- Endorsed as a skill on LinkedIn.

### GitHub Actions
- Endorsed as a skill on LinkedIn.

### Agile
- Provided mentorship on Agile velocity as Technical Advisor at StartX.
- Endorsed as a skill on LinkedIn.

### Scrum
- Provided mentorship on Scrum velocity as Technical Advisor at StartX.
- Endorsed as a skill on LinkedIn.

### Kanban
- Endorsed as a skill on LinkedIn.

### TDD
- Endorsed as a skill on LinkedIn.

### BDD
- Endorsed as a skill on LinkedIn.

### Playwright
- Endorsed as a skill on LinkedIn.

### ZeroMQ
- Messaging layer for Allele: Modular Genetic Micro-Trading Engine.
- Endorsed as a skill on LinkedIn.

### Qdrant
- Vector database implemented for persistent agent memory in the strata project.
- Endorsed as a skill on LinkedIn.

### Vector Databases
- Implemented in the strata project for persistent agent memory.
- Endorsed as a skill on LinkedIn.

### HFT (High Frequency Trading)
- Core domain for Allele: Modular Genetic Micro-Trading Engine.
- Endorsed as a skill on LinkedIn.

### Polymarket (CLOB)
- Allele HFT engine integrates with Polymarket Central Limit Order Book (CLOB).
- Endorsed as a skill on LinkedIn.

### Bitcoin
- Blockchain development at Joint Interagency Task Force.

### Monero
- Blockchain development at Joint Interagency Task Force.

### w3
- Interfaced traditional technologies with Ethereum's blockchain at Joint Interagency Task Force.

### MetaMask
- Interfaced traditional technologies with Ethereum's blockchain at Joint Interagency Task Force.

### Truffle
- Interfaced traditional technologies with Ethereum's blockchain at Joint Interagency Task Force.

### Angular
- Strong hands-on experience designing and developing web applications at Lowbush Company.

### Backbone.js
- Strong hands-on experience designing and developing web applications at Lowbush Company.
- Hands-on work at Marriott Vacation Club.

### Require.js
- Strong hands-on experience designing and developing web applications at Lowbush Company.
- Hands-on work at Marriott Vacation Club, converting web-reservation system.

### JavaScript
- Designed and developed JavaScript-based web applications at Lowbush Company.
- Built many JavaScript-based modules for the IBM Jam platform.
- Hands-on work at Marriott Vacation Club.
- Designed systems using JavaScript at AccessUSA (Hotelbeds).
- Built JavaScript-based UI for back office enterprise at AccessUSA.
- Hands-on development for Orlando.com / Internet Vacations.
- Hands-on development at Modis Technologies.

### HTML (HTML5)
- Strong hands-on experience at Lowbush Company (HTML5).
- Hands-on work at Marriott Vacation Club.
- Hands-on development for Orlando.com / Internet Vacations.
- Custom software development at Body International.
- Hands-on development at Modis Technologies.

### CSS (CSS3)
- Strong hands-on experience at Lowbush Company (CSS3).
- Hands-on work at Marriott Vacation Club.
- Hands-on development for Orlando.com / Internet Vacations.
- Custom software development at Body International.
- Hands-on development at Modis Technologies.

### REST (RESTful services)
- Strong hands-on experience at Lowbush Company.
- Converted web-reservation system to modern browser application built on top of JAX-RS and RESTful services at Marriott Vacation Club.
- Implemented new booking site utilizing REST.

### JEE
- Strong hands-on experience at Lowbush Company.
- Hands-on work at Marriott Vacation Club.
- Designed systems using JEE at AccessUSA (Hotelbeds).
- Used for custom software development at Body International.

### Twitter API
- Third party web platform integration at Lowbush Company.
- Gathered Twitter post data for IBM Social Media Aggregator (SMA).

### Salesforce.com
- Third party web platform integration at Lowbush Company.

### jQuery
- Hands-on work at Marriott Vacation Club.

### WebSphere
- Hands-on work at Marriott Vacation Club.
- Designed the WebSphere, MSSQL and Oracle upgrade strategy.
- Designed the strategy for migration to WebSphere clustering.

### DataPower
- Hands-on work at Marriott Vacation Club.

### JPA
- Hands-on work at Marriott Vacation Club.

### Servlets
- Hands-on work at Marriott Vacation Club.
- Used for custom software development at Body International.

### JDBC
- Hands-on work at Marriott Vacation Club.

### Eclipse
- Hands-on work at Marriott Vacation Club.
- Designed systems using Eclipse at AccessUSA (Hotelbeds).

### NetBeans
- Hands-on work at Marriott Vacation Club.

### Rational Application Developer
- Hands-on work at Marriott Vacation Club.

### Visio
- Hands-on work at Marriott Vacation Club.

### Mercurial
- Hands-on work at Marriott Vacation Club.
- Implemented distributed source code management at Marriott Vacation Club.

### Subversion
- Hands-on work at Marriott Vacation Club.
- Build and release managers maintained the base line in Subversion.

### Alfresco
- Hands-on work at Marriott Vacation Club.

### Oracle
- Hands-on work at Marriott Vacation Club.
- Designed the WebSphere, MSSQL and Oracle upgrade strategy.
- Designed systems using Oracle at AccessUSA (Hotelbeds).
- Used for custom software development at Body International.

### MSSQL
- Hands-on work at Marriott Vacation Club.
- Designed the WebSphere, MSSQL and Oracle upgrade strategy.
- Designed the strategy for migration to MSSQL clustering.
- Designed systems using MSSQL at AccessUSA (Hotelbeds).
- Hands-on development for Orlando.com / Internet Vacations.

### IIS
- Hands-on work at Marriott Vacation Club.
- Designed the strategy for migration to IIS clustering.
- Hands-on development for Orlando.com / Internet Vacations.

### MQSeries
- Hands-on work at Marriott Vacation Club.

### SOAP
- Hands-on work at Marriott Vacation Club.

### JAX-RS
- Hands-on work at Marriott Vacation Club.
- Converted web-reservation system to modern browser application built on top of JAX-RS.
- Implemented new package and preview booking site utilizing JAX-RS.

### JAX-WS
- Hands-on work at Marriott Vacation Club.

### JSON
- Hands-on work at Marriott Vacation Club.

### Omniture
- Analytical systems configuration at Lowbush Company.
- Hands-on work at Marriott Vacation Club.

### OpinionLab
- Hands-on work at Marriott Vacation Club.

### Google Analytics
- Analytical systems configuration at Lowbush Company.
- Hands-on work at Marriott Vacation Club.

### WCities
- Hands-on work at Marriott Vacation Club.

### ESB (Enterprise Service Bus)
- Hands-on work at Marriott Vacation Club.
- Architected the enterprise service bus (ESB) strategy to convert IT offerings into SOA.
- Designed and developed ESB strategy at Body International.

### SOA (Service-Oriented Architecture)
- Hands-on work at Marriott Vacation Club.
- Converted the enterprise’s IT offerings into a Service-Oriented architecture.
- Designed and built SOA strategy to provide web services for clients at AccessUSA (Hotelbeds).
- Designed and developed SOA strategy at Body International.

### BPEL
- Hands-on work at Marriott Vacation Club.

### WebLogic
- Designed systems using WebLogic at AccessUSA (Hotelbeds).

### Suse
- Designed systems using Suse at AccessUSA (Hotelbeds).

### Red Hat
- Designed systems using Red Hat at AccessUSA (Hotelbeds).

### Visual Studio
- Designed systems using Visual Studio at AccessUSA (Hotelbeds).

### Apache
- Designed systems using Apache at AccessUSA (Hotelbeds).

### .NET
- Hands-on development for Orlando.com / Internet Vacations.

### MSMQ
- Hands-on development for Orlando.com / Internet Vacations.

### BizTalk server
- Hands-on development for Orlando.com / Internet Vacations.

### JBoss
- Used for custom software development at Body International.

### OpenGL
- Hands-on development of simulation software at Modis Technologies.

### Open Inventor
- Hands-on development of simulation software at Modis Technologies.

### VRML
- Hands-on development of simulation software at Modis Technologies.

### Mathematica
- Hands-on development of simulation software at Modis Technologies.

### ObjectStore
- Hands-on development of simulation software at Modis Technologies.

### Genetic Algorithms
- Used in Allele: Modular Genetic Micro-Trading Engine.

### PowerShell
- Tech Stack for ARC-7.

### AST Parsing
- Uses AST parsing for ARC-7 Agentic Architecture Review Panel skill.

### Mixture-of-Models (MoM)
- Orchestrates a mixture-of-models review panel for ARC-7.

### LLM Orchestration
- Core functionality of ARC-7.

### TypeScript
- Tech Stack for strata.

### Embedding Models
- Implemented local embedding models for persistent agent memory in strata.


## Career Catalog

### DexCare: Principle Software Engineer / Director of Special Projects
**2021-Present**
**Role:**
Full stack development utilizing a mix of Node, Golang and Python toolchains to deliver healthcare solutions to large market medical companies such as Kaiser Permanente, Piedmont and CHN. Extensive use of technologies such as Kubernetes, RabbitMQ, Postgres, Splunk, DataDog. AI agent development utilizing tools such as Retool, Grok/GPT API, NodeRED, and n8n.
**Accomplishments:**
●​ Patent pending US20250103405A1 for distributed event based data platform: https://patents.google.com/patent/US20250103405A1/
●​ Designed and authored the best in class patient matching algorithm to reduce duplicate patient records rate while maintaining strict HIPAA compliance.
●​ Lead the DevCare effort to design and develop ephemeral developer environments that spin up DexCare’s entire software suite pinned to specific versions, utilizing Kubernetes, on machine technology clustering via Rancher Desktop as well as the ability to spin up cloud based and cloud agnostic deployments.
●​ Solutioned and managed DexCare’s Universal Authentication solution to position authentication and authorization at the transport layer thus reducing application complexity as well as streamlining auth for development and testing considerations.
●​ Acted as the primary mentor and instructor to development organization, designed and hosted educational sessions, 1 on one mentorship, workshops and self improvement workgroups.
**Metrics & Facts:**
- Millions of records, 80% reduction, 200k msg/sec, Petabyte-scale, $11B+ interdictions. (Note: DexCare specific: millions of records and transactions a day, CHN experienced a 80% reduction in false duplicate records).

### Technical Advisor - StartX
**2018-2020**
**Role:**
Advised early-stage founders on scalable systems architecture. Evaluated seed-stage technical stacks (React Native, Vue, WebSockets, gRPC). Provided mentorship on Agile and Scrum velocity.

### Joint Interagency Task Force: Principle Software Engineer / Government Projects Lead
**2015-2021**
**Role:**
Full stack development in traditional web technologies, Blockchain development for Bitcoin, Ethereum and Monero; and AI Agent development to aid the joint agencies in investigation and interdicting human and major drug trafficking events. Helped design tooling and build smart contracts to trace black market activity on various blockchains. I personally gained significant knowledge of Ethereum Smart Contracts, their implementation details and security weaknesses in the way contracts are written. I managed a team of 15 developers in various technology stacks, including Node.js and React for front and web-service technologies, Clojure for big data and integration work, as well as interfacing traditional technologies with Ethereum’s blockchain via w3, MetaMask, Truffle and oracles.
**Metrics & Facts:**
- Petabytes of data. Joint Interagency Task Force (JIATF-S) operations regularly interdict hundreds of millions of dollars in single offloads (e.g. $362M, $73M, $54M), scaling into the multi-billions annually across their operating theater.
- Millions of records, 80% reduction, 200k msg/sec, Petabyte-scale, $11B+ interdictions.

### Lowbush Company: Enterprise Architect / CTO
**2010-2015**
**Role:**
Full stack development consultancy, for clients such as Gartner, eCollege, EuroRSCG, and IBM. I design and develop JavaScript-based web applications, mobile solutions and Java middleware in this role. I also provide usability and A/B testing consultancy as well as analytical systems configuration such as Omniture and Google Analytics. This role requires strong hands-on experience with React, Node.js, Angular, Dojo, Backbone.js, Require.js, JavaScript, HTML5 CSS3, REST, Java, and JEE toolkits as well as third party web platform integrations such as twitter and Salseforce.com.
**Accomplishments:**
●​ Designed and developed the IBM Jam web application front end. JAM is a social conference platform that organizations such as NATO, the UN and various large corporations utilize to manage different types of assemblies. It provides forum, personal network, profile, chat, news, polls and a host of other functionalities. I personally designed the front-end strategy, as well as built many of the Dojo and JavaScript based modules for the platform.
●​ Designed and Developed the IBM Social Media Aggregator (SMA). SMA was a software solution that would aggregate social content about a conference taking place such as IBM LotusSphere. The system would via web services, gather blog data, Twitter post, Facebook Information, Flicker Images, YouTube videos as well as other third party data about a particular conference. It then provided a Dojo-based UI to display and aggregate all of this conference content into a feed. I personally designed the SMA, as well as wrote the entirety of the front end.

### Marriott Vacation Club: Senior Director of Technology
**2006-2010**
**Role:**
Provide and produce architecture and development requirements for Marriott’s web development and middleware team, as well as interface with business units to translate requirements into software blueprints for distribution to the development team. I provided hands-on development and oversight for UX initiatives as well as usability expertise. I worked with development teams to ensure code standards and understanding among the team. I managed defect resource assignment as well as provided resource estimates for project development and defect resolution. I lead the effort to identify and implement proper SCM tools including Source Control and defect tracking. I lead the effort to realign Release Management to fit into proper build and deployment enterprise controls. I worked hand on with the following tools and technologies: Dojo, jQuery, Backbone.js, Require.js, JavaScript, Java, JEE, WebSphere, DataPower, HTML, CSS, JPA, Servlets, JDBC, Eclipse, NetBeans, Rational Application Developer, Visio, Mercurial, Subversion, Alfresco, Oracle, MSSQL, IIS, MQSeries, SOAP, JAX-RS, JAX-WS, JSON, Omniture, OpinionLab, Google, WCities, ESB, SOA, BPEL.
**Accomplishments:**
●​ Guest speaker at IBM Impact 2009, discussing emerging web technologies and how to position the enterprise to take advantage of the changing landscape.
●​ Lead initiative to convert the entire web-reservation system over to a modern browser application that was built on top of Dojo, Require.js, JAX-RS and RESTful services.
●​ Salvaged project with a 10 million dollar overrun. Redesigned the system to account for legacy system performance issues, salvaging as much new development as possible, while completing the project in 4 months.
●​ Implemented new package and preview booking site utilizing web 2.0 and rich internet application technologies such as the Dojo Toolkit, REST and JAX-RS.
●​ Architected the enterprise service bus (ESB) strategy as well as the legacy application service architecture to convert the enterprise’s IT offerings into a Service-Oriented architecture.
●​ Designed strategy to build out of legacy systems while maintaining an existing level of service.
●​ Designed the organization's source control management strategy, implemented new source code management systems and processes to allow developers to use distributed source code management (Mercurial) while build and release managers maintained the base line in Subversion. Integrated defect tracking into the development process to ensure that all source code commits referred back to a ticket.
●​ Designed the WebSphere, MSSQL and Oracle upgrade strategy.
●​ Designed the strategy for migration to WebSphere, MSSQL and IIS clustering.
●​ Created a Standards and Conventions process for architectural documents (UML diagrams, Sequence diagrams, Entity Relationship diagram, Use Cases) as well as coding standards.

### AccessUSA (Hotelbeds): CTO / Director of Engineering
**2003-2006**
**Role:**
Responsible for executive decision-making on the architecture, design, development, testing and deployment of software systems. Management of development personnel, Project Management and estimating, software and hardware procurement, and communicating technical strategy to the executive team as well as the operations personnel, to ensure buy-in by all parties. I managed the technical direction of the company, as well as devised strategies to navigate the company out of several closed and exotic technologies that were constraining the business’s ability to grow. After acquisition, I acted as a liaison between US, Mallorcan, and other offshore teams to ensure that software standards and IT principals were upheld and ensured the information flow was unabridged. I worked hands-on and designed systems using the following tools and Technology: JavaScript,, Java, JEE, WebLogic, Oracle, Suse, Red Hat, C#, MSSQL, Eclipse, Visual Studio, Apache.
**Accomplishments:**
●​ Systematically phased out legacy systems while maintaining business initiatives, through IT planning and change management.
●​ built JavaScript-based UI for back office enterprise.
●​ Implemented Linux-based server farm to reduce overall IT systems investment.
●​ Designed and built SOA strategy to provide web services for clients such as Hotel.com, Expedia and Travelocity.
●​ Architected service framework for high availability, high load services to support all major travel sites.
●​ Responsible for repairing and decommissioning IT systems that lead the company to record profits and positioned the company for sale to First Choice Travel.
●​ Architected automation strategy to increase the percentage of bookings which required no human intervention from 40% to 92%.
●​ Streamlined employee system interface workflow, via usability testing, to reduce overall operational costs.

### Orlando.com / Internet Vacations: CTO / Principle Engineer
**2001-2003**
**Role:**
Executive technology planning, leadership, architecture and development for the travel website Orlando.com and online travel and accommodation booking site InternetVacations.com. Responsible for personnel management, budget, procurement, project planning, software design, development, testing and deployment of both sites. I was responsible for high-level technical strategy as well as low-level implementation details. I worked hands-on with the following tools and technologies: C#, .NET, IIS, MSSQL, MSMQ, JavaScript, HTML, CSS, BizTalk server, Credit Card processing API’s.
**Accomplishments:**
●​ Designed and built web property and hotel booking engine in 2 months.
●​ Took the company from start-up to acquisition by Hotels.com in 2 years.
●​ Designed technology systems to keep staffing levels low by automation.
●​ Designed and built data tracking systems, data analysis systems, search systems, online transaction payment systems, inventory management systems, content management system, web services, affiliates system, advertising management system.

### Body International: Lead Developer
**2000-2001**
**Role:**
Managing the technology strategies of Body International including: needs assessment, development cycle management, personnel management, and project management. Managed technical aspects and supporting systems for dietary supplement formulation research and development, manufacturing, inventory management, advertising (online, print, television), and magazine publishing. I also played an active role in custom software development for Body International using the following tools and technologies: Java, JEE, JBoss, Oracle, Servlets, HTML, CSS.
**Accomplishments:**
●​ Designed and Implemented COTS and custom technologies to integrate magazine publishing division, warehousing division, sales division and product research and development division.
●​ Designed and developed ESB and SOA strategy to align business around services (manufacturing, R&D, publishing, inventory, accounting) to allow COTS and custom development to coexist and utilize one another.
●​ Designed and implemented web presence as well as e-commerce and marketing systems.

### Modis Technologies: Sr. Simulations Developer / Team Lead
**1998-2000**
**Role:**
I was responsible for the architecture and design of simulation software including scene graph management, level design and artificial intelligence logic. I was responsible for mentoring other developers as well as managing their day-to-day tasks. Hands-on development with the following tools and technologies: C++, Java, OpenGL, Open Inventor, VRML, Mathematica, HTML, CSS, JavaScript, ObjectStore
**Accomplishments:**
●​ Designed an enemy combatant AI system that mimicked maneuvers to realistically emulate enemy strategies on the battlefield.
●​ Architected and implemented scene graph solutions such as object culling, viewport projection and collision detection.
●​ Architected and built a mass scale military intelligence battlefield simulator for the GuardRail project.
●​ Architected and built a radio transmission interception simulator for the EPLARS project.

### OCI: Senior Developer
**1995-1998**
**Role:**
I was responsible for the evaluation and implementation of new tools and technologies into the company’s offerings. I was tasked with evaluation technology; making recommendations as well as designing the processes and conventions around newly adopted technologies. I also participated in the development of ongoing projects as a secondary role.
**Accomplishments:**
●​ 3D design for the Naval F-14 tomcat and F-18 E&F simulator.
●​ Designed and deployed mass scale distributed training and simulation systems for the Naval F-14 and F-18 fighter jets.

### Project: Allele
**Role:**
Modular Genetic Micro-Trading Engine built for High Frequency Trading (HFT). Integrates with Polymarket Central Limit Order Book (CLOB). Leverages a ZeroMQ messaging layer, Redis for ultra-fast caching, and PostgreSQL for long-term genetic trait storage.
**Tech Stack:** Go, ZeroMQ, Redis, PostgreSQL, HFT, CLOB, Polymarket, Genetic Algorithms.

### Project: ARC-7
**Role:**
An Agentic Architecture Review Panel skill for runtime LLM environments. Uses AST parsing and local API integration to orchestrate a mixture-of-models review panel.
**Tech Stack:** PowerShell, AST Parsing, Mixture-of-Models (MoM), LLM Orchestration.

### Project: strata
**Role:**
3-Tier memory architecture (Global, Domain, Task) implementing the Qdrant vector database and local embedding models for persistent agent memory.
**Tech Stack:** TypeScript, Qdrant, Vector Databases, Embedding Models.

"""

with open(output_path, 'w') as f:
    f.write(md)

