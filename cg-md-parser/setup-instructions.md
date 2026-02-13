# 📦 Your Markdown Parsing Tool (cg-md-parser)

This is a complete package for parsing conversation markdown files using a local AI model (Ollama). 

**IMPORTANT**: You do **not** need Python installed. You only need **Docker Desktop**.

---

## 🚀 Step 1: Install Docker Desktop (If you don't have it)
1.  **Download**: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
2.  **Install & Start**: Run the installer and open Docker Desktop. Wait until the status bar at the bottom left is green (Engine running).

---

## 📥 Step 2: Load the Tool
You received a file named `cg-md-parser.tar`. This is the "packaged app".

1.  **Open Terminal / Command Prompt**:
    *   **Windows**: Press `Win + R`, type `powershell`, press Enter.
    *   **Mac**: Open `Terminal`.
2.  **Navigate to the file**:
    *   Example: `cd Downloads` (or wherever you saved the .tar file).
3.  **Run this command**:
    ```powershell
    docker load -i cg-md-parser.tar
    ```
4.  **Confirm**: You should see `Loaded image: cg-md-parser:latest`.

---

## 📂 Step 3: Prepare Your Folders
Create two folders on your Desktop (or anywhere easy to find):
1.  **Input Folder**: Put all your `.md` files here.
    *   Example: `C:\Users\You\Desktop\My_Inputs`
2.  **Output Folder**: Leave this empty. The tool will save results here.
    *   Example: `C:\Users\You\Desktop\My_Results`

---

## ▶️ Step 4: Run the Tool

The easiest way is to use the **Docker Desktop App** (Visual Interface).

1.  Open **Docker Desktop** and click the **Images** tab on the left.
2.  Find `cg-md-parser` in the list.
3.  Click the **Run** (Play icon) button next to it.
4.  Expand **Optional settings**:

    ### A. Connect Your Folders (Volume Mapping)
    You act as a bridge between your computer and the tool.
    *   **Host Path**: Click `...` and select your **Input Folder** (e.g., `Desktop\My_Inputs`).
    *   **Container Path**: Type exactly: `/input`
    *   *(Click the + button to add another row)*
    *   **Host Path**: Click `...` and select your **Output Folder** (e.g., `Desktop\My_Results`).
    *   **Container Path**: Type exactly: `/app/cg_md_output`

    ### B. Tell the Tool Where to Look (Environment Variable)
    *   Scroll down to "Environment variables".
    *   **Variable**: `INPUT_PATH`
    *   **Value**: `/input` 
        *   *(This tells the tool to process ALL files in the input folder)*

5.  Click **Run**.

---

## 👀 Step 5: See the Output
1.  Click on the container name (e.g., `trusting_curie`) in Docker Desktop to see the logs.
    *   **First Run Note**: If you see `Downloading model...`, please wait. It is downloading the required AI brain (about 2GB). This only happens once.
2.  Once logs say `[DONE] Process Complete`, open your **Output Folder** on your Desktop.
3.  You will see a new folder with results (organized by date/time).

---

## ⚡ Troubleshooting
*   **"Connection Refused"**: Ensure **Ollama** is running on your main computer. The tool talks to it.
*   **Permissions**: On Mac/Linux, if you get errors, ensure your input/output folders are accessible.
