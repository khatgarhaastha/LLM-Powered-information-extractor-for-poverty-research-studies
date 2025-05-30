## NOTE: This is my personal repo, the original repo for this project is private and is owned by Northwestern University


GPRL Data Entry Automation
===


## About the Project

This project was developed for the Global Poverty Research Lab (Kellogg School of Manangement, Northwestern University) under the supervision of Julius R. (Director of the Evidence to Policy Research Initiative,
Global Poverty Research Lab)

The project focuses on strealiming the data extraction process for the EPRI project and aims to eliminate the need for manual data extraction. The end goal of the Evidence to Policy Research Intiative being reducing the gap between poverty research findings and Policymakers' understanding and helping policymakers decide on the optimal way of designing financial aid packages. 

This project would help automate summarizing and finding key information data-points from Poverty research publication that would help the readers quickly understand effectiveness of treatments administered to various target groups across the globe. In essence, before the advent of this solution, workers would have to sit through long research papers to gather information about treatments and their effects reported under the paper. With this solution, data-summarization now takes less than a minute for each research paper compared to couple of days when done manually. 

To address the issue of cost-effectiveness for such a solution, we have designed 2 versions of this solution : 

- A Live service Version
- Batch processing Service

This allows the users to achieve the data-gathering and summarization output either as a stream job or as a batch job. 

![image](https://hackmd.io/_uploads/S15a_Pb9C.png)


Features
---

The project was developed in two phases: 



### Live Processing Components

1. **Front End**:
   - **User Interface**: Provides users with options to select the model (GPT-4 or Llama 3) for answer extraction.
   - **Accuracy Selection**: Allows users to choose the accuracy level, which adjusts how questions are batched for extraction. Higher accuracy results in fewer questions per API call, while lower accuracy batches more questions together.

2. **Model Selection and Answer Extraction Module**:
   - **Core Functionality**: Contains the essential source code for processing PDF documents and extracting answers.
   - **ExtractAnswers.py**: This Python file handles PDF processing and constructs prompts for both GPT-4 and Llama 3 models to extract relevant answers.

3. **Model and Front End Hosting using Docker**:
   - **Docker Containers**: 
     - **Front End Container**: Hosts the user interface.
     - **Backend Container**: Manages the backend logic and processes API calls from the front end.
     - **Model Container**: Hosts the Llama 3 model.
   - **Inter-Container Communication**: 
     - The front end sends API calls to the backend based on user selections.
     - The backend processes these requests and either communicates with the Llama 3 model container or sends API calls to OpenAI for GPT-4, depending on the selected model.
4. **MongoDB for storing Final answerCSVs**:
   - The Extracted answers are displaeys as a CSV file on the front end and the user can save the final csv in a mongo cluser or on their local device. 

   
This setup ensures seamless interaction between the front end, backend, and model containers, providing users with flexibility and efficiency in extracting answers from their documents.


### Batch Processing Components:

1. **Front End**:
   - **Technology Stack**: Built using Svelte and JavaScript.
   - **User Options**:
     - **Model Selection**: Users can choose between GPT-4 and Llama 3.1.
     - **Accuracy Level**: Users can select the accuracy level, which determines the number of questions per batch.
     - **PDF Upload**: Users can upload PDFs directly to an S3 bucket from the front end.
     - **Storage Options**: Users can either store the final CSV files in a MongoDB cluster or download them locally.

2. **Lambda Function**:
   - **Core Functionality**: This function handles the PDF processing and model prompt creation for GPT-4 and Llama 3.1.
   - **Trigger Mechanism**: The function is triggered when the user presses the extract button on the front end. It processes PDFs stored in the S3 bucket and extracts answers based on user input.

3. **AWS S3 for PDF and Question Storage**:
   - **PDF Storage**: PDFs are stored in an S3 bucket to be processed in batches.
   - **Question Storage**: Questions are stored in the S3 bucket, organized into batches according to different accuracy requirements.
   - **Processing Workflow**: The Lambda function retrieves PDFs and questions from the S3 bucket, processes them, and deletes the processed PDFs from the bucket.

4. **CI/CD with GitHub Actions and EC2**:
   - **Automation**: Code changes in the Lambda function or front end that are pushed to the GitHub repository are automatically reflected in the deployed Lambda function and front end (EC2).
   - **Deployment**: This ensures continuous integration and continuous deployment, making development more efficient.

5. **MongoDB for Storing Extracted Answer CSVs**:
   - **Final Storage**: Extracted answers are saved as CSV files in a designated MongoDB cluster for future reference.
   - **Access**: Users can access these CSVs directly from the front end.

This setup provides a comprehensive and automated solution for batch processing PDF documents, extracting answers using different models, and storing the results efficiently.

Deployment plan and How to access the Solution
---

Currently, the Live service version has been benched and we are serving only the batch processing solution. Below is the run down of the structure of the deployment and how the various systems interact with each other. 

You can access the Batch Processing Dashboard [Here](http://ec2-3-128-156-28.us-east-2.compute.amazonaws.com:8080/)

- **Frontend Application** : The Batch processing dashboard has been deployed on an EC2 instance. There is integration of CI/CD pipelines for this segment where code changes for the frontend are deployed instantly (triggered by Git Push) to EC2 instance using AWS CodeDeploy service. 
- **LLM Processing using AWS Lambda** : When a Data extraction request is triggered through options in Batch Processing Dashboard, a trigger is sent to AWS Lambda that hosts all the Processing code. Upon trigger, this segment pulls the uploaded papers from the AWS S3 and processes the documents as a batch using the options (of Model and Accuracy Selection) chosen at the time of trigger. 
- **AWS Bedrock** : We are using Bedrock service to access Meta's Llama 3.1 for text processing and OpenAI's APIs for access to GPT4. 



## Appendix and FAQ


1. What are the cost optimizations ? 

Before this solution, the project would require 2 coders to work full time and extract key datapoints from the paper, costing about $360 per paper. With this solution, we eliminated the work of redudant worker and essnetially reduced the costs by 60% overall. 



