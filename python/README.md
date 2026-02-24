# python-developer-test

## IDE and Tools
- I used `Jetbrains PyCharm` version 2025.3.2.1 for the development.
- I have the `JetBrains AI Assistant`, but I chose not to use it for this project.

## Project Setup
My choice of language version, tools, and libraries for the project are:
- `Python 3.12+` (3.12.12)
- `UV` for dependency management.
- `Ruff` for linting and formatting.
- `Bandit` for a first layer of security checks (I expect further security checks would happen in PR
processes and CI/CD pipelines).
- `pytest` and `coverage` for testing and code coverage metrics.

I set the project up to use `pyproject.toml` for a majority of the configuration, with some
specific configuration options specified in script commands used in my `tools/dev` scripts.

I created a `pre_push.sh` script to simplify the running of `uv`, `bandit`, and `ruff` checks,
along with unit tests and coverage metrics before pushing to the remote repository.

By using `pyproject.toml` and dev scripts it also means that in a team we're all running the same
checks and standardizing on the same configuration. The `pre_push.sh` script can optionally be
configured as a git pre-push hook, if desired.

The project setup includes a virtual environment, defaulting to the `.venv` directory (in the
project root and excluded from version control), ensuring everyone is using a project-specific environment
based on the project configuration.

## Project Requirements
- [Complete] Create a web crawler that will crawl a single domain and print out the URL of the page it is
crawling followed by the URLs it finds on that page.
- [Complete] The crawler will only process URLs for the same domain as the initially provided URL, ignoring
other domains and subdomains.
- [Partially] The crawler should run as quickly as possible, while not reducing accuracy or requiring
significant compute resources.
- [Complete] Tools that already do web crawling, such as Scrapy, cannot be used.
- [Complete] Tools that assist with functionality, such as HTML parsing, are allowed.

## Improvements
Some improvements I would like to make in the future for this kind of project include:
- Add a proper rate-limiting mechanism to prevent the crawler making too many requests too quickly.
  - The one I've got at the moment meets basic requirements, however, being able to limit to a number of requests
  per second properly would be more effective.
- Add detection and parsing of the robots.txt file to adjust rate limits as per the site policies and exclude
specific URLs.
- Add full error handling for the different Exceptions that can be raised, with proper feedback to the user if any
unresolvable errors occurred.
- Add detection and parsing of the sitemap.xml file to crawl URLs that can't be accessed from another page.
- Finish the unit testing to make sure all the critical areas are tested and increase the coverage to the
required level.
- Add support for handling redirects to only crawl the latest version of a page.
- Add support for multiple domains, by moving the existing `Crawler` class out to a new `Spider` class and adding
logic to the `Crawler` class to create a `Spider` for each domain, with its own rate limits.
- Add a proper output mechanism to have result output to a structured file or database, instead of printing to the CLI,
as the CLI output is largely useless and unwieldy in this kind of scenario unless you're piping the output to another
CLI tool for filtering/transformation, or other processing.

## In Hindsight
### What went well?
- I've gotten the main functionality working with clear modular functions that are easy to maintain long-term, with
 docstring comments for the public functions.
- I chose to perform HEAD requests for each URL to check the declared content-type header before making a GET request
to the valid content for crawling, this helps with reducing bandwidth usage and avoiding unnecessary requests to pages
that are not `text/html`.
  - This would also ideally be expanded with additional filtering based on other (currently unknown) project
  requirements, such as using URL filtering to completely ignore image files if there is no requirement to crawl
  potentially hidden content.
- The number of HTTP requests are limited by default to a maximum of 10 at a time which helps with rate limiting
to an initial level, until further improvements are made.
- I was also able to get some unit testing in place for some of the logic, showing the way I like to structure
and write my unit tests.

### What could have gone better?
During the development I was definitely overthinking what you were wanting to see, and that resulted in unnecessary
time spent on refactoring and rewriting parts. Doing this again, I would spend the first 10-15 minutes deciding on a
strategy and then stick to it for the duration, unless something significantly wrong was discovered with my original
choice.

In a scenario with less time constraint, I would also have done TDD, so the logic is tested as I develop it.

Using an AI tool would definitely have meant faster progress with more time to finish unit tests and other in-progress
aspects of the project, however, that would also have obfuscated my mindset and approach to the tasks and so may not be
suitable for use here.

---

---

---

# Zego

## About Us

At Zego, we understand that traditional motor insurance holds good drivers back.
It's too complicated, too expensive, and it doesn't reflect how well you actually drive.
Since 2016, we have been on a mission to change that by offering the lowest priced insurance for good drivers.

From van drivers and gig economy workers to everyday car drivers, our customers are the driving force behind everything we do. We've sold tens of millions of policies and raised over $200 million in funding. And we’re only just getting started.

## Our Values

Zego is thoroughly committed to our values, which are the essence of our culture. Our values defined everything we do and how we do it.
They are the foundation of our company and the guiding principles for our employees. Our values are:

<table>
    <tr><td><img src="../doc/assets/blaze_a_trail.png?raw=true" alt="Blaze a trail" width=50></td><td><b>Blaze a trail</b></td><td>Emphasize curiosity and creativity to disrupt the industry through experimentation and evolution.</td></tr>
    <tr><td><img src="../doc/assets/drive_to_win.png?raw=true" alt="Drive to win" width=50></td><td><b>Drive to win</b></td><td>Strive for excellence by working smart, maintaining well-being, and fostering a safe, productive environment.</td></tr>
    <tr><td><img src="../doc/assets/take_the_wheel.png?raw=true" alt="Take the wheel" width=50></td><td><b>Take the wheel</b></td><td>Encourage ownership and trust, empowering individuals to fulfil commitments and prioritize customers.</td></tr>
    <tr><td><img src="../doc/assets/zego_before_ego.png?raw=true" alt="Zego before ego" width=50></td><td><b>Zego before ego</b></td><td>Promote unity by working as one team, celebrating diversity, and appreciating each individual's uniqueness.</td></tr>
</table>

## The Engineering Team

Zego puts technology first in its mission to define the future of the insurance industry.
By focusing on our customers' needs we're building the flexible and sustainable insurance products
and services that they deserve. And we do that by empowering a diverse, resourceful, and creative
team of engineers that thrive on challenge and innovation.

### How We Work

- **Collaboration & Knowledge Sharing** - Engineers at Zego work closely with cross-functional teams to gather requirements,
  deliver well-structured solutions, and contribute to code reviews to ensure high-quality output.
- **Problem Solving & Innovation** - We encourage analytical thinking and a proactive approach to tackling complex
  problems. Engineers are expected to contribute to discussions around optimization, scalability, and performance.
- **Continuous Learning & Growth** - At Zego, we provide engineers with abundant opportunities to learn, experiment and
  advance. We positively encourage the use of AI in our solutions as well as harnessing AI-powered tools to automate
  workflows, boost productivity and accelerate innovation. You'll have our full support to refine your skills, stay
  ahead of best practices and explore the latest technologies that drive our products and services forward.
- **Ownership & Accountability** - Our team members take ownership of their work, ensuring that solutions are reliable,
  scalable, and aligned with business needs. We trust our engineers to take initiative and drive meaningful progress.

## Who should be taking this test?

This test has been created for all levels of developer, Junior through to Staff Engineer and everyone in between.
Ideally you have hands-on experience developing Python solutions using Object Oriented Programming methodologies in a commercial setting. You have good problem-solving abilities, a passion for writing clean and generally produce efficient, maintainable scaleable code.

## The test 🧪

Create a Python app that can be run from the command line that will accept a base URL to crawl the site.
For each page it finds, the script will print the URL of the page and all the URLs it finds on that page.
The crawler will only process that single domain and not crawl URLs pointing to other domains or subdomains.
Please employ patterns that will allow your crawler to run as quickly as possible, making full use any
patterns that might boost the speed of the task, whilst not sacrificing accuracy and compute resources.
Do not use tools like Scrapy or Playwright. You may use libraries for other purposes such as making HTTP requests, parsing HTML and other similar tasks.

## The objective

This exercise is intended to allow you to demonstrate how you design software and write good quality code.
We will look at how you have structured your code and how you test it. We want to understand how you have gone about
solving this problem, what tools you used to become familiar with the subject matter and what tools you used to
produce the code and verify your work. Please include detailed information about your IDE, the use of any
interactive AI (such as Copilot) as well as any other AI tools that form part of your workflow.

You might also consider how you would extend your code to handle more complex scenarios, such a crawling
multiple domains at once, thinking about how a command line interface might not be best suited for this purpose
and what alternatives might be more suitable. Also, feel free to set the repo up as you would a production project.

Extend this README to include a detailed discussion about your design decisions, the options you considered and
the trade-offs you made during the development process, and aspects you might have addressed or refined if not constrained by time.

# Instructions

1. Create a repo.
2. Tackle the test.
3. Push the code back.
4. Add us (@nktori, @danyal-zego, @bogdangoie, @cypherlou and @marliechiller) as collaborators and tag us to review.
5. Notify your TA so they can chase the reviewers.
