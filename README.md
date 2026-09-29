[1. Webhook: /analyze-data] 

          │ (Receives uploaded file)
          ▼

[2. Extract from File] 

          │ (Reads tabular records)
          ▼

[3. Edit Fields] 

          │ (Formats necessary attributes)
          ▼

[4. JavaScript Code Node] 
 
          │ (Batches 1,000 items into 1 array)
          ▼

[5. HTTP Request: host.docker.internal:8000] 
 
          │ (Python computes exact statistics & correlations)
          ▼
          
[6. Basic LLM Chain + Ollama (Llama 3.2 3B)] 
          
          │ (Generates 10-point grounded analytical report)
          ▼
          
[Final Clean Analytics Summary]
