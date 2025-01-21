import os

from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import (EXCLUDED_DIRS, EXCLUDED_EXTENSIONS,
                     INCLUDED_LANGUAGE_WITH_EXTENSION,
                     OTHER_ALLOWED_CONFIG_EXT)


def read_file(path: str) -> str:
    """
    Read the contents of a file.

    Args:
        path (str): The path to the file to be read.

    Returns:
        str: The contents of the file, or an error message if reading fails.
    """
    try:
        with open(path, mode="r", encoding="utf-8") as reader:
            return reader.read()
    except Exception as e:
        return f"Error reading {path}: {str(e)}"


def get_every_file_content_in_folder(folder_path: str, is_code: bool, repo_link: str):
    """
    Get the content of every file in a folder and its subfolders, with chunks and metadata.

    Args:
        folder_path (str): The path to the folder to read.
        is_code (bool): Whether to include code files only.
        repo_link (str): The link to the repository.

    Returns:
        AgentResponse: A dictionary containing:
            - 'content': The concatenated content of all files.
            - 'chunks': List of content chunks.
            - 'metadata': List of metadata for each chunk.
    """
    if not os.path.exists(folder_path):
        raise ValueError(f"Folder '{folder_path}' does not exist.")

    all_contents = ""
    chunks = []
    repo_name = repo_link.split("/")[-1]
    repo_creator_name = repo_link.split("/")[3]
    for root, dirs, files in os.walk(folder_path):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        file_end_delimiter = "\n\n" + "*" * 50 + "EOF" + "*" * 50 + "\n\n"
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension not in EXCLUDED_EXTENSIONS:
                file_path = os.path.join(root, file)
                file_content = read_file(file_path)
                file_content += f"Location: {file_path}\n{file_content}\n\n"
                file_content += file_end_delimiter
                all_contents += file_content
                if is_code:
                    ext = file_extension[1:]
                    if ext in INCLUDED_LANGUAGE_WITH_EXTENSION:
                        code_chunks = chunk_code(file_content, ext, 1000)
                        chunks.extend(code_chunks)
                    elif ext in OTHER_ALLOWED_CONFIG_EXT:
                        code_chunks = chunk_text(file_content, 500)
                        chunks.extend(code_chunks)

                    # chunk_id += 1
    return dict(
        content=all_contents,
        chunks=chunks,
        repo_name=repo_name,
        repo_creator_name=repo_creator_name
    )


def write_file(data: str) -> None:
    """
    Write data to a file named 'output.txt'.

    Args:
        data (str): The data to be written to the file.
    """
    with open("output.txt", mode="+a", encoding="utf-8") as writer:
        writer.write(data)


def chunk_code(content: str, ext: str, context_size: int) -> list:
    """
    Split code content into chunks using a language-specific splitter.

    Args:

        content (str): The code content to be split.
        ext (str): The file extension indicating the programming language.
        context_size (int): The desired size of each chunk.

    Returns:
        list: A list of code chunks.
    """
    if ext == 'rs':
        ext = 'rust'
    if ext == 'c++':
        ext = 'cpp'
    if ext == 'cs':
        ext = 'csharp'
    splitter = RecursiveCharacterTextSplitter.from_language(
        language=ext,
        chunk_size=context_size,
        chunk_overlap=0
    )
    splits = splitter.create_documents([content])
    return [split.page_content for split in splits]


def chunk_text(content: str, context_size: int = 1000) -> list:
    """
    Split text content into chunks using RecursiveCharacterTextSplitter.

    Args:
        content (str): The text content to be split.
        context_size (int, optional): The desired size of each chunk. Defaults to 1000.

    Returns:
        list: A list of text chunks, or an empty list if chunking fails.

    Example:
        >>> text = "This is a long document that needs to be split into smaller chunks..."
        >>> chunks = chunk_text(text, context_size=500)
    """
    if not content or not isinstance(content, str):
        print("Invalid input: content must be a non-empty string")
        return []

    try:
        # Configure the text splitter with appropriate parameters
        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=context_size,
            # 10% overlap between chunks
            chunk_overlap=int(context_size * 0.1),
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
            # length_function=len,
            is_separator_regex=False
        )

        # Create document chunks
        splits = splitter.create_documents([content])

        # Extract the text content from each split
        chunks = [split.page_content for split in splits]

        # Validate the output
        if not chunks:
            print("Warning: No chunks were generated from the input text")
            return []

        return chunks

    except Exception as e:
        print(f"Error chunking text: {str(e)}")
        return []
