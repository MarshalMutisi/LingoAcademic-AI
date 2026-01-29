import os
from execution.llm_utils import call_llm
from execution.file_utils import read_file, save_file, extract_text_from_pdf
from execution.search_utils import perform_search, format_search_dossier
from execution.status_logger import log_status

def run_pipeline(input_source, max_iterations=2):
    log_status("Initializing LingoAcademic AI...", progress=5)
    print("--- Starting LingoAcademic AI Pipeline (Librarian Edition) ---")
    
    # Check if input is a PDF or TXT file
    if input_source.lower().endswith(".pdf"):
        log_status("Analyzing PDF content...", progress=10)
        input_text = extract_text_from_pdf(input_source)
        if input_text.startswith("Error"):
            log_status(f"Error: {input_text}", status="error")
            return
    elif input_source.lower().endswith(".txt") and os.path.exists(input_source):
        log_status("Reading source file...", progress=10)
        input_text = read_file(input_source)
    else:
        input_text = input_source

    # 1. Load Directives
    log_status("Loading agent SOPs...", progress=15)
    research_sop = read_file("directives/research_agent.md")
    writer_sop = read_file("directives/writer_agent.md")
    critic_sop = read_file("directives/critic_agent.md")
    
    # 2. Librarian Phase: Grounding
    log_status("Librarian is searching for German sources...", progress=20)
    print("\n[Librarian Phase] Researching German sources...")
    query_prompt = f"English Source Text: {input_text}\n\nTask: Generate a single optimized German academic search query to find relevant literature/frameworks for this topic."
    search_query = call_llm(query_prompt, system_prompt=research_sop)
    if search_query.startswith("Error"):
        log_status(f"Librarian failed: {search_query}", status="error")
        return
    
    log_status(f"Searching for: {search_query}", progress=30)
    raw_results = perform_search(search_query)
    dossier = format_search_dossier(raw_results)
    save_file(".tmp/research_dossier.md", dossier)
    log_status("Research grounding dossier prepared.", progress=40)

    current_content = f"### Source Material\n{input_text}\n\n{dossier}"
    current_draft = ""

    for i in range(max_iterations):
        progress_base = 40 + (i * 30)
        log_status(f"Iteration {i+1}: Writer is drafting...", progress=progress_base + 5)
        print(f"\n[Iteration {i+1}]")
        
        # Step A: Writer Agent
        writer_prompt = f"Grounding Research & Source Material: {current_content}\n\nExisting Draft: {current_draft}\n\nPlease follow the SOP and provide the next version of the German academic text. Use the research sources for citations where relevant."
        current_draft = call_llm(writer_prompt, system_prompt=writer_sop)
        if current_draft.startswith("Error"):
            log_status(f"Writer failed: {current_draft}", status="error")
            return
        
        save_file(f".tmp/draft_v{i+1}.md", current_draft)
        
        # Step B: Critic Agent
        log_status(f"Iteration {i+1}: Critic is auditing...", progress=progress_base + 15)
        critic_prompt = f"Current Draft: {current_draft}\n\nPlease audit this text according to the German academic standards in your SOP. Provide status [APPROVED] or [REVISION REQUIRED] and specific feedback."
        feedback = call_llm(critic_prompt, system_prompt=critic_sop)
        if feedback.startswith("Error"):
            log_status(f"Critic failed: {feedback}", status="error")
            return
        
        save_file(f".tmp/feedback_v{i+1}.md", feedback)
        
        if "[APPROVED]" in feedback.upper():
            log_status("Critic approved the draft!", progress=95)
            break
        else:
            log_status(f"Revision required for Iteration {i+1}.", progress=progress_base + 25)
            # Keep research grounding even in revisions
            current_content = f"Feedback from Critic: {feedback}\nOriginal Intent & Research: {current_content}"
            
    # Final Output
    save_file("final_academic_output.md", current_draft)
    log_status("LingoAcademic AI pipeline completed.", progress=100, status="completed")
    print("\n--- Pipeline Completed. Final output saved to final_academic_output.md ---")

if __name__ == "__main__":
    import sys
    # Use command line arg or default test
    source = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    if not os.path.exists(source) and (source.endswith(".pdf") or source.endswith(".txt")):
        print(f"Warning: {source} not found. Using default text test.")
        source = "The impact of encryption on digital privacy in the 21st century."
        
    run_pipeline(source)
