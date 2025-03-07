def get_readme_prompt(batch_number: int, total_batches: int, previous_analysis, chunks) -> str:

    return f'''# Context Analysis
Analyze the following code chunks (batch {batch_number}/{total_batches}) and identify:
- Core functionality and patterns
- Key dependencies and external services used
- Configuration requirements
- API endpoints and their purposes
- Database schemas and models
- Environment variables used
- Installation dependencies

Add this information to the existing analysis from previous batches. If this is the first batch, start fresh.

{previous_analysis}

# Current Code Chunks
```
{chunks}
```

# Required Output
Based on the cumulative analysis of all code chunks seen so far, generate or update the following README sections:

## Project Overview
- Identify the primary purpose and functionality
- Note the main technologies and frameworks used
- Highlight key features and capabilities

## Features and Implementation
- List all identified features
- Explain how each feature works
- Document API endpoints (if present)
- Describe data models and relationships

## Local Development Setup
- List all prerequisites
- Provide step-by-step installation instructions
- Include any database setup requirements
- Note any external service dependencies

## Environment Variables
If environment variables are detected, create a .env.example template:
```
# Required Variables
VARIABLE_NAME=example_value # Brief description of purpose

# Optional Variables
OPTIONAL_VAR=default_value # Description and when needed
```

Base Rule:
- Do not include anything else apart from the contents of README.md
- Generate strictly in Markdown format
- Do not  include anything related to internal process. Directly give the resultant contents of the file.

Correct Example:
```
# Project Overview
This project is a web application that allows users to create and share notes. It is built using the Django framework and uses a PostgreSQL database for data storage. The application provides a RESTful API for note management and user authentication.
```

Incorrect Example:
```
The following code is for as follows:
....
```

## Generation Rules
1. Maintain consistency with previous batches
2. Update existing sections when new relevant information is found
3. Add new sections only for newly discovered major features
4. Keep technical details accurate and concise
5. Format using clear Markdown structure
6. Include code examples for critical setup steps
7. Generate comprehensive yet readable documentation
8. Highlight any security-sensitive configuration

Remember: This is an iterative process. Each batch may reveal new information that requires updating previous sections. Maintain a cohesive narrative throughout the README.
'''
