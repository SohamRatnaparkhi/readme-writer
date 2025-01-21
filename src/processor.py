from .chunking import get_every_file_content_in_folder
from .git_operations import clone_git_repo
from .llm import get_gemini_response
from .prompt import get_readme_prompt


async def process_repo_to_get_readme(repo_link):
    try:
        status, path = clone_git_repo(repo_link)
        if not status:
            return {"error": path}
        repo_data = get_every_file_content_in_folder(
            folder_path=path, is_code=True, repo_link=repo_link
        )

        content, chunks, repo_name, creator = repo_data["content"], repo_data[
            "chunks"], repo_data["repo_name"], repo_data["repo_creator_name"]

        window = 20

        total_batches = len(chunks) // window
        batches = 0

        prev_analysis = ""

        for i in range(0, len(chunks), window):
            chunk_window = chunks[i:i + window]
            chunk_text = "\n ---------- \n".join(chunk_window)
            current_prompt = get_readme_prompt(
                batch_number=batches + 1,
                total_batches=total_batches,
                previous_analysis=prev_analysis,
                chunks=chunk_text,
            )

            prev_analysis = await get_gemini_response(current_prompt)
            batches += 1
        print(prev_analysis)
        return {
            "repo_name": repo_name,
            "creator": creator,
            "readme": prev_analysis
        }
    except Exception as e:
        return {"error": str(e)}
