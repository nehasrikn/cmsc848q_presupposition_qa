
# Experiment Outline

## Experiment 1: Replicate Kim et. Al
Pipeline: Google unanswerable questions + Paired Gold Document --> FEVER (5 sentences) --> Evaluation

## Experiment 2: Expand Pool of Documents via Hyperlinks
Pipeline: Google unanswerable questions + Paired Gold Document + All Documents hyperlinked from gold document--> FEVER (5 sentences) --> Evaluation

## Experiment 3: DPR with Unanswerable Question
Pipeline: Google unanswerable questions --> DPR --> Retrieve top n passages --> FEVER with passages as "documents" (5 sentences) --> Evaluation

## Experiment 4: DPR with direct presuppositions
Pipeline: Google unanswerable question's presuppositions --> DPR --> Retrieve top n passages --> FEVER with passages as "documents" (5 sentences) --> Evaluation

## Experiment 5: Question Generation for Larger Document Pool 
Pipeline: Google unanswerable questions --> RoleQG (generate k questions, each question to DPR) --> Pool all passages from DPR on top of k questions --> FEVER (5 sentences) --> Eval